import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


login_manager = LoginManager()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)


login_manager.init_app(app)
#로그인 사용자를 관리하는 애플리케이션 구성 

login_manager.login_view = "login"
# 실제 app.py파일에서 뷰를 설정할 때 login이라는 뷰를 생성하고 이 login_manager와 연결하여 사용자가 
# 어떤 뷰를 클릭해서 로그인하면 되는지 알려주는 것 
