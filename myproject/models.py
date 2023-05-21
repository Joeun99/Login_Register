#사용자 정보를 저장하는데 필요한 모든 설정을 함


from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
#UserMixin : 이 클래스의 속성을 상속받으면 다양한 내장 속성에 엑세스할 수 있고 실제 뷰에서 호출할 수 있다.
#사용자 로그인 및 권한 부여 등 모든 관리 기능을 가진다. 



#Flask-Login이 현재의 사용자를 로드하고 ID를 가져올 수 있게 함
#누군가 로그인하면 로그인 ID에 특정된 페이지를 보여줄 수 있음(내 정보 같은 페이지?)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
# 사용자 데이터베이스에서 해당 사용자 ID를 쿼리하고 가져온 결과를 반환합니다.
# 사용자 ID를 근거로 현재 사용자를 로드하는 기능이 있다는 의미.
# 사용자 ID를 근거로 사용자 테이블을 쿼리하고 해당 사용자를 가져옴. -> 해당 사용자에게 특정 정보를 보여줄 수 있음




class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    # 두 명의 사용자가 같은 이메일을 사용하지 못하도록 unique = True
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    #재로그인할 떄 저장된 비밀번호의 '해시값'과 방금 입력한 비밀번호의 '해시값'을 비교해서 일치하면 로그인 성공!
