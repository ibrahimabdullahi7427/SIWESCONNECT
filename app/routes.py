from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User
from app.forms import RegisterForm, LoginForm
from app.recommender import get_recommendations

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('An account with that email already exists.', 'danger')
            return redirect(url_for('main.register'))
        user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            course=form.course.data,
            state=form.state.data,
            opportunity_type=form.opportunity_type.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome back, ' + user.full_name + '!', 'success')
            return redirect(url_for('main.dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    recommendations = get_recommendations(
        course=current_user.course,
        state=current_user.state,
        opportunity_type=current_user.opportunity_type,
        top_n=70
    )
    return render_template('dashboard.html', recommendations=recommendations)


@main.route('/seed-database-now-siwesconnect')
def seed_db():
    from app.models import Organisation
    import sys
    sys.path.insert(0, '.')
    from seed import organisations
    Organisation.query.delete()
    db.session.commit()
    for org in organisations:
        db.session.add(org)
    db.session.commit()
    return f"Successfully seeded {len(organisations)} organisations."