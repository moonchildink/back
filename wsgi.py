from app import creat_app, db
import os

os_name = os.name
if os_name == 'nt':
    app = creat_app()
elif os_name == 'posix':
    if os.uname()[1] == 'moonchild':
        app = creat_app(config_name='wsl')
    app = creat_app(config_name='deploy')

with app.app_context():
    db.create_all()
