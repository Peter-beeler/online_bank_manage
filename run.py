# encoding: utf-8
from bank import app,db
from flask_login import LoginManager
if __name__ == '__main__':
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'message'

    db.create_all()
    app.run()