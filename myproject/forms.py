from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
# 유효성 검사기
# DataRequired : 폼의 특정 필드를 공백으로 둘 수 없다는 의미
# Email : 이메일을 사용하고 있는지 (@ 기호가 있는지 확인 , .org 또는 .com으로 끝나는지 확인)
# EqualTo : 비밀번호 확인에 사용됨(회원가입시 사용자가 비밀번호를 잘못 입력하지 않았는지 확인)
from wtforms import ValidationError
# 유효성 검사 오류


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='비밀번호가 일치하지 않습니다.')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()]) #비밀번호 한번 더 입력(확인하게끔)
    submit = SubmitField('회원가입!')




    # 등록된 이메일인지 체크하는 부분
    # 사용자 테이블을 쿼리한 후 전달된 데이터 필드(이메일 데이터)와 일치하는 이메일이 있는지 확인하는 것
    # 만약에 있다면 그 이메일은 1개밖에 없을것이므로 첫 번째 이메일을 가져온다.
    # 만약에 해당 이메일이 존재하는 경우 ValidationError로 유효성 검사 오류를 실행한다  
    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('이미 등록된 이메일입니다!')

    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('이미 등록된 사용자 이메일입니다!')
