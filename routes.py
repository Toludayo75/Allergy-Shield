from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm import joinedload
from app import app, db
from models import User, Product, Allergen, UserAllergen, ProductIngredient
from forms import LoginForm, RegistrationForm, ProfileForm, SearchForm

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('home'))
        flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered')
            return render_template('register.html', form=form)
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
            flash('Registration successful!')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.')
    return render_template('register.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    allergens = Allergen.query.all()
    form.allergens.choices = [(str(a.id), a.name) for a in allergens]

    if form.validate_on_submit():
        try:
            # Update user allergens efficiently
            UserAllergen.query.filter_by(user_id=current_user.id).delete()
            new_allergens = [UserAllergen(user_id=current_user.id, allergen_id=int(aid)) 
                           for aid in form.allergens.data]
            db.session.bulk_save_objects(new_allergens)
            db.session.commit()
            flash('Profile updated successfully!')
            return redirect(url_for('profile'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to update profile. Please try again.')

    # Pre-select current allergens
    if request.method == 'GET':
        form.allergens.data = [str(ua.allergen_id) for ua in current_user.allergens]

    return render_template('profile.html', form=form)

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        query = form.query.data.strip()
        try:
            # Optimize query with joins
            products = Product.query.options(
                joinedload(Product.ingredients)
            ).filter(
                (Product.name.ilike(f'%{query}%')) | 
                (Product.nafdac_number == query)
            ).all()

            # Get user allergens once
            user_allergen_ids = {ua.allergen_id for ua in current_user.allergens}

            for product in products:
                allergen_ingredients = []
                safe_ingredients = []

                for ingredient in product.ingredients:
                    if ingredient.is_allergen:
                        allergen_ingredients.append(ingredient.ingredient_name)
                    else:
                        safe_ingredients.append(ingredient.ingredient_name)

                # Check if product contains user's allergens
                is_safe = not bool(set(allergen_ingredients) & user_allergen_ids)

                results.append({
                    'product': product,
                    'allergen_ingredients': allergen_ingredients,
                    'safe_ingredients': safe_ingredients,
                    'is_safe': is_safe
                })
        except Exception as e:
            flash('Error occurred during search. Please try again.')

    return render_template('search.html', form=form, results=results)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))