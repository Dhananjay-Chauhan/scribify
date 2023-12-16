from sqlalchemy import func
from zoooop import app
from flask import render_template, flash, request, redirect, url_for
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
import bcrypt
from zoooop.models.User import *   
from zoooop.models.Blog import *   
from zoooop.models.Blog_Action import *  
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user




login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



    

@app.route("/")
def index():
    return render_template('base.html',title='current_user.name')


@app.route("/register" ,methods=['GET','POST'])
def register():
    if request.method == "POST":
        # print(request.form)
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        phone_number = request.form['phone_number']
        # password = request.form['password']
        password = request.form['password']
        hash_password = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode(); 
        user = Users(name=name, username=username,email=email,password=hash_password,phone_number=phone_number)
        db.session.add(user)
        db.session.commit() 
        flash('Registered Successfully.')
        return redirect(url_for('register'))
    
  
    return render_template('register.html')


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form['username'] 
        password = request.form['password']
        hash_password = Users.query.filter_by(username=username).first()
        print(hash_password.password.encode())
        if bcrypt.checkpw(password.encode(),hash_password.password.encode()):
            flash(f'You were successfully logged as username : {username}')
            login_user(hash_password)
            return render_template('base.html',login_state='true')
        else:
            flash('Wrong username or password ! Retry') 


    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    flash(f'You were successfully logged out as username : {current_user.name}')
    logout_user()
    return redirect(url_for('login'))

@app.route("/post",methods=['GET','POST'])
@login_required
def posts():
    if request.method == "POST":
        title=request.form['title']
        author=request.form['author']
        content=request.form['content']
        tags=request.form['tags']
        slug=request.form['slug']
        blog = Blogs(title=title,author=author,content=content,tags=tags,slug=slug, user_id=current_user.user_id)
        db.session.add(blog)
        db.session.commit() 
        flash('Blog Posted Successfully.')
        return redirect(url_for('posts'))
    
    return render_template('post.html')


@app.route("/blogs",methods=['GET','POST'])
def postBlog():
    like_counts = db.session.query(Blogs_Action.post_id, func.count(Blogs_Action.action_id).label('like_count')) \
    .filter(Blogs_Action.likes == True) \
    .group_by(Blogs_Action.post_id) \
    .all()
    dislike_counts = db.session.query(Blogs_Action.post_id, func.count(Blogs_Action.action_id).label('dislike_count')) \
    .filter(Blogs_Action.dislikes == True) \
    .group_by(Blogs_Action.post_id) \
    .all()
    # for post_id, count in like_counts:
    #     print(f'The count of likes for post {post_id} is: {count}')
    all_blogs = Blogs.query.all()
    # all_likes =
    like_ = {key:value for key,value in like_counts}
    dislike_ = {key:value for key,value in dislike_counts}
    return render_template('blogs.html',all_blogs=all_blogs,like_=like_,dislike_=dislike_)

@app.route("/like/<int:my_integer>/", methods=['GET', 'POST'])
def like(my_integer):
    if request.method == "POST":
        chk = Blogs_Action.query.filter_by(post_id=my_integer,user_id=current_user.user_id).first()
        likes=False
        if chk is None:
            likes=True
            blog_action = Blogs_Action(post_id=my_integer,likes=likes,dislikes=False,user_id=current_user.user_id)
            db.session.add(blog_action)
        else:
            if chk.dislikes==True or chk.likes==False :
                likes=True
            chk.likes=likes;
            chk.dislikes=False;     
        db.session.commit() 
        return redirect(url_for('postBlog'))
    

@app.route("/dislike/<int:my_integer>/", methods=['POST'])
def dislike(my_integer):
    if request.method == "POST":
        chk = Blogs_Action.query.filter_by(post_id=my_integer,user_id=current_user.user_id).first()
        dislikes=False
        if chk is None:
            dislikes=True
            blog_action = Blogs_Action(post_id=my_integer,likes=False,dislikes=dislikes,user_id=current_user.user_id)
            db.session.add(blog_action)
        else:
            if chk.likes==True or chk.dislikes==False :
                dislikes=True
            chk.likes=False;
            chk.dislikes=dislikes;     
        db.session.commit() 
        return redirect(url_for('postBlog'))


@app.route("/read_blog/<int:id>",methods=['GET','POST'])
def read_blog(id):
    like_counts = db.session.query(Blogs_Action.post_id, func.count(Blogs_Action.action_id).label('like_count')) \
    .filter(Blogs_Action.likes == True) \
    .group_by(Blogs_Action.post_id) \
    .all()
    dislike_counts = db.session.query(Blogs_Action.post_id, func.count(Blogs_Action.action_id).label('dislike_count')) \
    .filter(Blogs_Action.dislikes == True) \
    .group_by(Blogs_Action.post_id) \
    .all()

    like_ = {key:value for key,value in like_counts}
    dislike_ = {key:value for key,value in dislike_counts}
    blogs =  Blogs.query.filter_by(post_id=id).first()

    blog_content = blogs.content
    blog_title = blogs.title
    blog_post_id = blogs.post_id

    return render_template('read_blog.html',blog_content = blogs.content,blog_title = blogs.title,like_=like_,dislike_=dislike_,blog_post_id = blogs.post_id)


@app.route("/user_profile",methods=['GET','POST'])
@login_required
def user_profile():

    if request.method == 'POST':
        new_name=request.form['name']
        new_email=request.form['email']
        new_phone_number=request.form['phonenumber']


        user = Users.query.filter_by(user_id=current_user.user_id).first()
        user.name=new_name
        user.email=new_email
        user.phone_number=new_phone_number
        db.session.commit()
        return render_template('user_profile.html',current_user=current_user)


    return render_template('user_profile.html',current_user=current_user)

@app.route("/my_blogs",methods=['GET','POST'])
@login_required
def my_blogs():

    like_counts = db.session.query(Blogs_Action.post_id, func.count(Blogs_Action.action_id).label('like_count')) \
    .filter(Blogs_Action.likes == True) \
    .group_by(Blogs_Action.post_id) \
    .all()
    dislike_counts = db.session.query(Blogs_Action.post_id, func.count(Blogs_Action.action_id).label('dislike_count')) \
    .filter(Blogs_Action.dislikes == True) \
    .group_by(Blogs_Action.post_id) \
    .all()

    all_blogs = Blogs.query.filter_by(user_id=current_user.user_id)
    # all_likes =
    like_ = {key:value for key,value in like_counts}
    dislike_ = {key:value for key,value in dislike_counts}
    return render_template('my_blogs.html',all_blogs=all_blogs,like_=like_,dislike_=dislike_)


@app.route("/update_blog/<int:post_id>",methods=['GET','POST'])
@login_required
def update_blog(post_id):
    if request.method == 'POST':
        new_title=request.form['title']
        new_author=request.form['author']
        new_tags=request.form['tags']
        new_slug=request.form['slug']
        new_content=request.form['content']
        blog = Blogs.query.filter_by(user_id=current_user.user_id,post_id=post_id).first()
        blog.title=new_title
        blog.author=new_author
        blog.tags=new_tags
        blog.slug=new_slug
        blog.content=new_content
        db.session.commit()
        return redirect(url_for('my_blogs'))
     
    blog = Blogs.query.filter_by(user_id=current_user.user_id,post_id=post_id).first()
    return render_template('update_blog.html',post_id=post_id,blog=blog)





