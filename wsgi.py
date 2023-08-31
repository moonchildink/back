from app import creat_app,db

app = creat_app()


with app.app_context():
    db.create_all()