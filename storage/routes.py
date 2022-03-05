from storage import app
from flask import render_template, redirect, url_for, flash, request
from storage.models import Item, User
from storage.forms import RegisterForm, LoginForm, PossessItemForm, ReturnItemForm
from storage import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def homepage():
    return render_template('home.html')


@app.route('/cargo_hold', methods=['GET', 'POST'])
@login_required
def cargo_hold():
    possess_form = PossessItemForm()
    return_form = ReturnItemForm()

    if request.method == "POST":
        # purchasing item db
        possessed_item = request.form.get('possessed_item')
        p_item_object = Item.query.filter_by(name=possessed_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.possess(current_user)
                flash(f'You possessed {p_item_object.name}', category='success')
            else:
                flash(f'You cannot afford for {p_item_object.name}', category='danger')
        # returning item db
        returned_item = request.form.get('returned_item')
        r_item_object = Item.query.filter_by(name=returned_item).first()
        if r_item_object:
            if current_user.can_return(r_item_object):
                r_item_object.returning(current_user)
                flash(f'You returned {r_item_object.name} to our vault.', category='success')
            else:
                flash(f'You cannot return item, that you are not possess.', category='danger')
        return redirect(url_for('cargo_hold'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('cargo_hold.html', items=items, possess_form=possess_form,
                               owned_items=owned_items, return_form=return_form)


@app.route('/registration', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password_01.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Successfully registered! You are now logged in as {user_to_create.username}.', category='info')
        return redirect(url_for('cargo_hold'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a new user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success log in as: {attempted_user.username}!', category='success')
            return redirect(url_for('cargo_hold'))
        else:
            flash('Username and password are not match! Correct your input.', category='danger')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with login procedure: {err_msg}', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been log out!', category='info')
    return redirect(url_for('homepage'))
