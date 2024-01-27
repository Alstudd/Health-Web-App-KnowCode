from io import BytesIO
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from .models import User, Upload
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, login_user, current_user, logout_user
from werkzeug.utils import secure_filename
# from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
import random
import string

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        key = str(password)
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, key):
                flash('Logged In Successfully!', category='success')
                login_user(user, remember=True)
                if user.id != 1:
                    return redirect('/')
                else:
                    return redirect('/admin')
            else:
                flash('Incorrect password!, Try Again!', category='error')
        else:
            flash('Email does not exist!', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        image_file = request.files['image_file']
        print(image_file)
        image_mimetype = image_file.mimetype
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2= request.form.get('password2')
        emerEmail = request.form.get('emerEmail')
        emerNumber = request.form.get('emerNumber')
        mail = str(email)
        uname = str(username)
        pass1 = str(password1)
        user = User.query.filter_by(email=email).first()
        my_name = User.query.filter_by(username=username).first()
        if user:
            flash('Email already exists!', category='error')
        elif my_name:
            flash('Username already exists!', category='error')
        elif not image_file:
            flash('No image uploaded', category='error')
        elif len(mail) < 4: 
            flash('Email must be greater than 3 characters.', category='error')
        elif len(uname) < 2: 
            flash('Username must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(pass1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            path = os.path.join(auth.root_path, "static/profile_pics")
            image_type = image_file.mimetype
            i = len(image_type) - 1
            final = ""
            while(image_type[i] != "/"):
                final = final + image_type[i]
                i = i - 1
            filetype = final[::-1]
            result = str(request.form.get('username')) + "." + filetype
            fullpath = os.path.join(path, result)
            image_file.save(fullpath)

            letters = string.ascii_lowercase 
            uniqueUserCode = ''.join((random.choice(letters)) for x in range(10)) 

            # add user to database
            new_user = User(unique = uniqueUserCode, filetype = filetype, image_file = result, image_data=image_file.read(), image_mimetype=image_mimetype, email=email, username=username, password=generate_password_hash(pass1), emerEmail=emerEmail, emerNumber=emerNumber)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            Upload(my_name="", age="", dob="", gender="", height="", weight="", blood_grp="", heart_attack="", region="", pincode="", allergies="", medic="", past_medic="", user_id=current_user.id)
            if new_user.id != 1:
                new_user.person = "User"
                db.session.add(new_user)
                db.session.commit()
                parent_dir = os.path.join(auth.root_path, "static/storage")
                my_dir = new_user.username
                my_path = os.path.join(parent_dir, my_dir)
                os.mkdir(my_path)
                parent_dir2 = os.path.join(auth.root_path, "static/insurance")
                my_dir2 = new_user.username
                my_path2 = os.path.join(parent_dir2, my_dir2)
                os.mkdir(my_path2)
                return redirect('/')
            else:
                new_user.person = "Admin"
                db.session.add(new_user)
                db.session.commit()                
                return redirect('/admin') 
    return render_template("signup.html", user=current_user)