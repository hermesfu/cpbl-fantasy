from .user import user_bp
from .player import player_bp
from .league import league_bp

def register_blueprints(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(player_bp)
    app.register_blueprint(league_bp)