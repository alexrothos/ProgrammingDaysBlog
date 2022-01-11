from flask import render_template

from app import app, db
from app.errors import bp

# TODO - No need of these too <--- I will keep these for a while for testing
# will delete them later...
@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500