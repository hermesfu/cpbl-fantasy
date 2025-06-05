from .user import user_bp
from .player import player_bp
from .league import league_bp
from .team import team_bp
from .requirement import requirement_bp
from .roster import roster_bp

def register_blueprints(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(player_bp)
    app.register_blueprint(league_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(requirement_bp)
    app.register_blueprint(roster_bp)
