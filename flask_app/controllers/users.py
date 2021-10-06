from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']) #request.form['password']  was used to test the login 
                                                                            #once Bcrypt was implemented all users need to be deleted and create again                             
    }
    id = User.save(data)
    session['user_id'] = id

    return redirect('/home')   #

@app.route('/userlogin',methods=['POST'])
def userlogin():
    user = User.get_user_by_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/home')


@app.route('/home')
def dashboard():

    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("home.html",user=User.get_user_by_id(data),recipes=Recipe.get_all_recipes())





@app.route('/logout')
def logout():
        session.clear()
        return redirect('/')