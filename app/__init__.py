from flask import Flask
from app.api.routes import apiBlueprint

def createApp():
    app = Flask(__name__, static_folder="../app/static")
    app.register_blueprint(apiBlueprint)

    # Configurar la carpeta estática para servir archivos como index.html
    @app.route('/<path:path>')
    def staticFiles(path):
        return app.send_static_file(path)

    return app
