from app import creat_app,db

app = creat_app(config_name='deploy')
with app.app_context():
    db.create_all()