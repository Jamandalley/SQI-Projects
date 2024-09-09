from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
from App.config import Config, db, login_manager
from App.routes import auth, customer, account, transaction

# db = SQLAlchemy()
# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth.bp, url_prefix='/auth')
    app.register_blueprint(customer.bp, url_prefix='/customer')
    app.register_blueprint(account.bp, url_prefix='/account')
    app.register_blueprint(transaction.bp, url_prefix='/transaction')

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    return app