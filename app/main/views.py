from flask import render_template,request,redirect,url_for, flash
from . import main
from .. import db, login_manager
from ..models import User, Pitch,Comment, Category
from flask_login import login_user, current_user, logout_user, login_required


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def make_pitches(pitches):

  new_pitches = []
  for pitch in pitches:
    user = User.query.filter_by(id=pitch.user_id).first()
    category = Category.query.filter_by(id=pitch.category_id).first()
    comments = Comment.query.filter_by(pitch_id=pitch.id).all()
    new_pitches.append({
      'id': pitch.id,
      'title': pitch.title,
      'content': pitch.content,
      'category': category,
      'user': user,
      'upvotes': pitch.upvotes,
      'downvotes': pitch.downvotes,
      'comments': len(comments)
    })
  return new_pitches


@main.route('/')
def index():
  categories = Category.query.order_by(Category.id.asc()).all()
  pitches = Pitch.query.order_by(Pitch.id.desc()).all()
  new_pitches = make_pitches(pitches)
  return render_template('pages/index.html', categories=categories, pitches=new_pitches)


@main.route('/pitches/categories/<string:category_id>')
def category_view(category_id):
  category = Category.query.filter_by(id=category_id).first()
  categories = Category.query.order_by(Category.id.asc()).all()
  print("category", category)
  if category:
    pitches = Pitch.query.filter_by(category_id=category.id).all()
    new_pitches = make_pitches(pitches)
    return render_template('pages/category.html', categories=categories, category=category, pitches=new_pitches)
  else:
    flash('Category not found', 'warning')
    return redirect(url_for('main.index'))


@main.route('/pitches/view/<string:pitch_id>/')
@login_required
def pitch_view(pitch_id):
  pitch = Pitch.query.filter_by(id=pitch_id).first()
  if pitch:
    comments = Comment.query.filter_by(pitch_id=pitch.id).all()
    new_comments = []
    for comment in comments:
      user = User.query.filter_by(id=comment.user_id).first()
      new_comments.append({
        'id': comment.id,
        'content': comment.content,
        'user': user,
        'created_at': comment.created_at
      })
    user = User.query.filter_by(id=pitch.user_id).first()
    return render_template('pages/pitches/pitchview.html', pitch=pitch, comments=new_comments, user=user)
  else:
    flash('Pitch not found', 'warning')
    return redirect(url_for('main.index'))


@main.route('/pitches/view/<string:pitch_id>/comments/add/', methods=['GET', 'POST'])
@login_required
def add_comment(pitch_id):
  pitch = Pitch.query.filter_by(id=pitch_id).first()
  if request.method == 'POST':
    content = request.form['comment']
    if pitch:
      comment = Comment(pitch_id=pitch.id, user_id=current_user.id, content=content)
      db.session.add(comment)
      db.session.commit()
      flash('Comment added', 'success')
      return redirect(url_for('main.pitch_view', pitch_id=pitch.id))
    else:
      flash('Pitch not found', 'warning')
      return redirect(url_for('main.index'))
  return redirect(url_for('main.pitch_view', pitch_id=pitch.id))


# Upvote a pitch and return redirect to the referer
@main.route('/pitches/view/<string:pitch_id>/upvote/', methods=['GET', 'POST'])
@login_required
def upvote_pitch(pitch_id):
  pitch = Pitch.query.filter_by(id=pitch_id).first()
  if pitch:
    pitch.upvotes += 1
    db.session.commit()
    flash('Pitch upvoted', 'success')
    return redirect(request.referrer)
  else:
    flash('Pitch not found', 'warning')
    return redirect(url_for('main.index'))


@main.route('/pitches/view/<string:pitch_id>/downvote/', methods=['GET', 'POST'])
@login_required
def downvote_pitch(pitch_id):
  pitch = Pitch.query.filter_by(id=pitch_id).first()
  if pitch:
    pitch.downvotes -= 1
    db.session.commit()
    flash('Pitch downvoted', 'success')
    return redirect(request.referrer)
  else:
    flash('Pitch not found', 'warning')
    return redirect(url_for('main.index'))


@main.route('/pitches/new/', methods=['GET','POST'])
@login_required
def new_pitch():
  categories = Category.query.order_by(Category.id.asc()).all()
  if request.method == 'POST':
    pitch = Pitch(title=request.form['title'], content=request.form['content'], category_id=request.form['category'], user_id=current_user.id)
    db.session.add(pitch)
    db.session.commit()
    flash('Pitch created successfully', 'success')
    return redirect(url_for('main.index'))
  
  return render_template('pages/pitches/addpitch.html', categories=categories)

@main.route('/auth/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
      login_user(user)
      flash('User Logged in', 'success')
      return redirect(url_for('main.index'))
    else:
      return redirect(url_for('main.login'))
      flash('Login failed', 'danger')
  return render_template('pages/auth/login.html', title='Login')


@main.route('/auth/signup', methods=['GET','POST'])
def signup():
  if request.method == 'POST':
    if request.form['password'] == request.form['rpassword']:
      new_user = User(username=request.form['username'],
                      email=request.form['email'],
                      fullname=request.form['fullname'],
                      bio=request.form['bio'],
                      password=request.form['password'])
      db.session.add(new_user)
      db.session.commit()
      flash('User created successfully', 'success')
      return redirect(url_for('main.login'))
    else:
      flash('Passwords do not match', 'danger')
    return redirect(url_for('main.signup'))
  return render_template('pages/auth/signup.html', title='Sign Up')


@main.route('/auth/profile', methods=['GET','POST'])
@login_required
def profile():
  my_pitches = Pitch.query.filter_by(user_id=current_user.id).all()
  new_pitches = make_pitches(my_pitches)
  return render_template('pages/auth/profile.html', title='My Profile', pitches=new_pitches)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@main.route('/pitches/categories/new/', methods=['GET','POST'])
@login_required
def new_category():
  if request.method == 'POST':
    new_category = Category(name=request.form['name'])
    try:
      db.session.add(new_category)
      db.session.commit()
      flash('Category created successfully', 'success') 
    except:
      flash('Category already exists', 'danger')
  return render_template('pages/pitches/addcategory.html', title='New Category')
