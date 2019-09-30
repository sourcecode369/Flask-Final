
import os
import glob
from my_project import app, db
from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user
from my_project.models import User
from my_project.forms import LoginForm, RegistrationForm

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("you logged out.!")
    return redirect(url_for('home'))


@app.route("/updw")
def updw():
    files = glob.glob("uploads/**")
    print(files)
    return render_template("up_dw.html",file = files)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/success", methods=['GET', 'POST'])
def success():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        f = request.files['file']

        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if f and allowed_file(f.filename):
            filename = f.filename
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            f.save(f.filename)
            return render_template("success.html", name=f.filename)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Logged in successfully.!')
            next = request.args.get('next')
            if next is None or not next[0] == '/':
                next = url_for('welcome_user')
            return redirect(next)
    return render_template("login.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data
                    )
        db.session.add(user)
        db.session.commit()
        flash("You have been registered successfully.")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/users')
def all_users():
    users = User.query.all()
    user = {}
    for i, u in enumerate(users):
        user[i] = (u.username, u.email)
    print(user.values())
    return render_template('list_users.html', users=list(user.values()))


if __name__ == "__main__":
    app.run(debug=True)
