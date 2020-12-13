from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    
    #Initializing Flask Extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    simple.init_app(app)
    

    # Creating the app configurations
    app.config.from_object(config_options[config_name])
    
     # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/authenticate')
    
    # configure UploadSet
    configure_uploads(app,photos)
    


    return app