import os

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY = 'dev',
    #     DATABASE = os.path.join(app.instance_path, 'apps.sqlite')
    # )
    
    from . import home, learning, auth, stock_market
    app.register_blueprint(home.bp)
    app.register_blueprint(learning.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(stock_market.bp)
    
    return app