# encoding: utf-8

from bank import app,db
if __name__ == '__main__':
    db.create_all()
    app.run()