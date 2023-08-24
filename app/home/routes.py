import os
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.home import blueprint
from app import db
from app.models import User, Document
from sqlalchemy import or_
from app.home.forms import UpdateUserForm, DocumentForm
from werkzeug.utils import secure_filename
from app.utils import UPLOAD_PATH


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
    pages = 5
    documents = Document.query.filter().paginate(page, per_page=pages, error_out=False)
    for doc in documents.items:
        print(doc)
        
    form = DocumentForm()

    if (form.validate_on_submit()):
        document_file = form.document.data
        filename = secure_filename(document_file.filename)
        path = os.path.join(UPLOAD_PATH, filename)
        document_file.save(path)

        # Create a new Document instance and save it to the database
        document = Document(file_name=form.file_name.data, path=path, user_id=current_user.id,
                            created_by=current_user.id, updated_by=current_user.id)
        db.session.add(document)
        db.session.commit()

        flash('Document uploaded successfully', 'success')
        return redirect(url_for('home.add_document', page=page, continue_flag=continue_flag))

    return render_template('add_document.html', user=user, form=form, documents=documents, continue_flag=continue_flag, title="Documents")
