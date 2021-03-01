from flask import Flask
from TicTacToe.config import Config


def create_app(config_file=Config):
    app=Flask(__name__)

    app.config.from_object(Config)
    from TicTacToe.main.routes import main
    from TicTacToe.game.routes import game
    app.register_blueprint(main)
    app.register_blueprint(game)

    return app