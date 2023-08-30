import os, tempfile
import time
from flask import render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app.home import blueprint
from app import db
from app.models import User, Document
from sqlalchemy import or_
from app.home.forms import UpdateUserForm, DocumentForm
from werkzeug.utils import secure_filename
from app.utils import UPLOAD_PATH, encrypt_file, decrypt_file


@blueprint.route('/')
@login_required
def index():
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('index.html', user=user)


@blueprint.route('/transaction', methods=['GET', 'POST'])
@login_required
def transaction():
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('transaction.html', user=user)


@blueprint.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)


@blueprint.route('/edit-profile/<username>', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = UpdateUserForm()
    
    if (form.validate_on_submit()):
        form.populate_obj(user)  # Update user's attributes with form data
        
        db.session.commit()
        
        flash('Profil berhasil diperbaharui', 'success')
        return redirect(url_for('home.profile', username=user.username))
    
    flash("Profil gagal diperbaharui!", 'danger')
    return render_template('edit_profile.html', form=form, user=user)


@blueprint.route('/add_document', methods=['GET', 'POST'], defaults={"page":1, "continue_flag":"No"})
@login_required
def add_document(page, continue_flag):
    user = User.query.filter_by(username=current_user.username).first()
    page = page
    continue_flag = continue_flag
    pages = 20
    documents = Document.query.filter().paginate(page, per_page=pages, error_out=False)
        
    form = DocumentForm()

    if (form.validate_on_submit()):
        start_time = time.time()  # Record start time
        document_file = form.document.data
        filename = secure_filename(document_file.filename) + ".enc"
        path = os.path.join(UPLOAD_PATH, filename)
        
        encryption_key = form.encryption_key.data
        
        encrypt_file(encryption_key, document_file.read(), path)
        
        # Create a new Document instance and save it to the database
        document = Document(file_name=form.file_name.data, path=path, user_id=current_user.id,
                            created_by=current_user.id, updated_by=current_user.id)
        db.session.add(document)
        db.session.commit()
        
        end_time = time.time()  # Record end time
        processing_time = end_time - start_time

        flash(f'Document uploaded and encrypted successfully', 'success')
        print(f'Log_info: Document uploaded and encrypted successfully. Time taken: {processing_time:.4f} seconds')
        return redirect(url_for('home.add_document', page=page, continue_flag=continue_flag))

    return render_template('add_document.html', user=user, form=form, documents=documents, continue_flag=continue_flag, title="Documents")


@blueprint.route('/download/<int:document_id>', methods=['GET', 'POST'])
@login_required
def download_document(document_id):
    start_time = time.time()  # Record start time
    document = Document.query.get_or_404(document_id)

    # Extract the original filename and extension
    original_filename = os.path.basename(document.path)
    
    # Create a temporary file with the original filename and extension
    temp_file_path = os.path.join(tempfile.gettempdir(), original_filename)
    temp_file_path = temp_file_path.replace(".enc", "")

    # Decrypt the content using the user-provided encryption key
    decryption_key = request.form.get('decryption_key')
    
    decrypted_content, error_status = decrypt_file(decryption_key, document.path)

    if error_status == True:
        flash('Cannot decrypt selected document', 'error')
        return redirect(url_for('home.add_document', page=1, continue_flag="No"))
    
    # Write the decrypted content to the temporary file
    with open(temp_file_path, 'wb') as temp_file:
        temp_file.write(decrypted_content)
    
    end_time = time.time()  # Record end time
    processing_time = end_time - start_time
    
    print(f'Log_info: Document downloaded and decrypted successfully. Time taken: {processing_time:.4f} seconds')
    
    # Send the temporary file as an attachment
    return send_file(temp_file_path, as_attachment=True)

@blueprint.route('/delete_document/<int:document_id>', methods=['GET', 'POST'])
@login_required
def delete_document(document_id):
    document = Document.query.get_or_404(document_id)
    
    # Delete the file associated with the document
    if os.path.exists(document.path):
        os.remove(document.path)

    # Delete the document from the database
    db.session.delete(document)
    db.session.commit()

    flash('Document deleted successfully', 'success')
    return redirect(url_for('home.add_document', page=1, continue_flag="No"))