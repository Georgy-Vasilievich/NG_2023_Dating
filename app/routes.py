"""Flask routes"""

from app import app

from app.dating import dating_bp
from app.login import login_bp
from app.logout import logout_bp
from app.register import register_bp
from app.rules import rules_bp
from app.settings import settings_bp

app.register_blueprint(dating_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(register_bp)
app.register_blueprint(rules_bp)
app.register_blueprint(settings_bp)
