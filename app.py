from myproject import app,db
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user
from myproject.models import User
from myproject.forms import LoginForm, RegistrationForm
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')
#사용자가 로그인 했을 때 환영해줌, 사용자가 이 view를 보려면 로그인이 되어 있어야함
#로그인 하지 않은 상태에서 welcom_user.html을 방문하려고 하면 로그인 페이지로 리디렉션되고 로그인하라는 메시지 표시

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('로그아웃 됐어요!')
    return redirect(url_for('home'))
# 사용자가 로그아웃하려는 경우 이 페이지에 오도록
# 이것을 보려면 로그인이 되어 있어야 한다. -> @login_required


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()
        # 사용자 모델 테이블에서 사용자를 가져오는 것
        # 로그인을 위해 제공한 이메일을 기반으로 사용자를 가져옴 

        if user.check_password(form.password.data) and user is not None:
            # model.py의 check_password 메서드 사용.
            # if문 뜻  : 비밀번호가 정확하고 제공된 사용자가 존재하는가?
            login_user(user)
            flash('성공적으로 로그인!')

            next = request.args.get('next')
            # 만약 로그인이 필요한 페이지를 사용자가 방문하려고 한다면 next로 저장
            # 로그인을 하지 않은 사용자가 welcome_user에 액세스하는 경우 Flask는 해당 페이지에 대한 요청을 
            # next 페이지로 저장후 LoginForm으로 리디렉션

            if next == None or not next[0]=='/':
                next = url_for('welcome_user')
                
            # 만약 정상적으로 로그인한 상태였다면 사용자가 가려고 했던 next 페이지를 요청
            # next 페이지에 아무것도 없을 떄(로그인한 상태니까 next에 쌓인 요청이 없음)
            # welcome_user

            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('회원가입을 성공하였습니다!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
