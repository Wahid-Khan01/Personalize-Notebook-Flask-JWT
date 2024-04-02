from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

x = 'D^1sB],>tJ!q>fwLEqLAx>[YXD&jWN^D,bZq,mN]MTH[({uhz[WKpXnASj{<]MP#^|H*tmV.wb?>NGLLbLvAhvSSNrb,++#DcVzANda>:{w%MV+SL{@#Hn(Muke*<}k)Do[gOjWcii^NmuEPa+:?dL%pip$mIT#u_IMwI[uPz<?!*ET+g@KNTBfWhp{GNVJJT&kV:V_Gdb$!<:+tH{kfWgMhog>;c[Yy)>jb)m?W%SAy:rYZ{<H.$k]GvG<SV;XL'

db = SQLAlchemy()
dbname = 'notebook.db'
def create_database(app, db):
    if not path.exists(f'instance/{dbname}'):
        with app.app_context():
            db.create_all()
            print('database created')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = x
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{dbname}'
    db.init_app(app)
    
    from .Authorization.controllers.logout import logout
    app.register_blueprint(logout, url_prefix='/api/auth/')
    from .Authorization.controllers.login import login
    app.register_blueprint(login, url_prefix='/api/auth/')
    from .Authorization.controllers.signup import signup
    app.register_blueprint(signup, url_prefix='/api/auth/')
    
    from .notes.controllers.notebook import foo
    app.register_blueprint(foo, url_prefix='/api/notes/')
    
    create_database(app, db)
    
    return app