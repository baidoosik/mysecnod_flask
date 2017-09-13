import threading
from flask import render_template, session, redirect, url_for,flash, abort
from flask_login import login_required,current_user
from .. import db
from ..models import User,Role,Post,Permission
from ..email import Mail
from . import blog
from .forms import PostForm
from ..decorator import admin_required, permission_required

@blog.route('/post/new', methods=['GET', 'POST'])
@login_required
def post_new():
    form = PostForm()

    if current_user.can(Permission.WRITE_ARTICLES) and \
        form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author_id=current_user.id)
        db.session.add(post)
        flash('The new post register!')
        return redirect(url_for('main.index'))


    return render_template('blog/post_new.html',form=form)

@blog.route('/post/list', methods=['GET', 'POST'])
@login_required
def post_list():
    post_qs = Post.query.all()

    return render_template('blog/post_list.html',{
        'post_list':post_qs
    })


@blog.route('/post/detail/<int:id>', methods=['GET'])
@login_required
def post_detail(id):
    post = Post.query.get_or_404(id)
    return render_template('blog/post_detail.html',post=post)

@blog.route('/post/edit/<int:id>', methods=['GET','Post'])
@login_required
def post_edit(id):
    post = Post.query.get_or_404(id)

    if current_user !=post.author and \
        not current_user.can(Permission.ADMINISTER):
        abort(403)
    form =PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.add(post)
        flash('the post is editted !')
        return redirect(url_for('blog.post_detail',id=post.id))

    form.content.data = post.content
    form.title.data = post.title

    return render_template('blog/post_edit.html',form=form)
