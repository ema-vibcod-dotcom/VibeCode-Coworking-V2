from flask import Flask, redirect, url_for
from config import Config
from database import db
from controllers.admin_controller import admin_bp
from controllers.user_controller import user_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    from controllers.reservation_controller import reservation_bp
    app.register_blueprint(reservation_bp)

    @app.route('/')
    def index():
        return redirect(url_for('user.login'))

    return app

if __name__ == '__main__':
    app = create_app()
    print(app.url_map)
    app.run(debug=True, port=5001)
