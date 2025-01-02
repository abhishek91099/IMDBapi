from flask import Flask
from config import config
from database import db
from routes import bp

def create_app():
    app = Flask(__name__)
    app.config.update(config)
    
    db.init_app(app)
    app.register_blueprint(bp,url_prefix='/movies')
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)