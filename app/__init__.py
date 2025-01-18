from flask import Flask

def createApp():
    app = Flask(__name__)

    from app.api.routes import apiBlueprint
    app.register_blueprint(apiBlueprint, url_prefix = '/api')

    return app