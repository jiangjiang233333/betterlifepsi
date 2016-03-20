# encoding=utf-8

import os

from flask import Flask, request, current_app, render_template
from flask.ext.login import current_user
from flask.ext.migrate import upgrade
import config
import database


def create_app(custom_config=None):
    flask_app = Flask(__name__, template_folder='templates', static_folder='static')

    if custom_config is None:
        import app.config as default_config
        flask_app.config.from_object(default_config.ProductionConfig)
    else:
        flask_app.config.from_object(custom_config)

    return flask_app


def init_flask_security(flask_app, database):
    from flask_security import SQLAlchemyUserDatastore, Security
    from app.models.security import User, Role
    import app.config as config
    for key, value in config.BaseConfig.security_messages.items():
        flask_app.config['SECURITY_MSG_' + key] = value
    user_datastore = SQLAlchemyUserDatastore(database, User, Role)
    from views.login_form import LoginForm
    Security(flask_app, user_datastore, login_form=LoginForm)


def init_admin_views(flask_app, database):
    from app.views import init_admin_views
    init_admin_views(flask_app, database)


def init_db(flask_app):
    from app.database import DbInfo
    from flask_sqlalchemy import SQLAlchemy
    sqlalchemy = SQLAlchemy(flask_app)
    sqlalchemy.init_app(flask_app)
    DbInfo.set_db(sqlalchemy)
    return sqlalchemy


def init_migrate(flask_app, database):
    from flask.ext.migrate import Migrate
    migrate = Migrate(app=flask_app, db=database)
    with flask_app.app_context():
        upgrade(directory=os.path.dirname(__file__) + "/../migrations")


def init_babel(flask_app):
    from flask_babelex import Babel
    # return Babel(default_locale='zh_Hans_CN', app=flask_app)
    return Babel(app=flask_app)


def init_logging(flask_app):
    from raven.contrib.flask import Sentry
    # Init Sentry if not in debug mode
    if flask_app.config['DEBUG'] or flask_app.config['TESTING']:
        Sentry().init_app(flask_app)
    else:
        # Set log level to debug and redirect all the logs to stand out
        import logging
        from logging import StreamHandler
        log_handler = StreamHandler()
        flask_app.logger.setLevel(logging.DEBUG)
        flask_app.logger.addHandler(log_handler)

        # Disable werkzeug log
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)


def init_debug_toolbar(flask_app):
    from flask.ext.debugtoolbar import DebugToolbarExtension
    if flask_app.config['DEBUG']:
        flask_app.debug = True
        DebugToolbarExtension(flask_app)


def define_route_context(flask_app, db, babel):
    from werkzeug.utils import redirect

    @flask_app.route('/report')
    def report():
        return render_template('report.html')

    @flask_app.route('/')
    def hello():
        return redirect("/admin", code=302)

    @flask_app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @babel.timezoneselector
    def get_timezone():
        if getattr(current_user, 'timezone', None) is not None:
            return current_user.timezone.code
        return 'CST' if current_app.config['DEBUG'] else "UTC"

    @babel.localeselector
    def get_locale():
        """
        Put your logic here. Application can store locale in
        user profile, cookie, session, etc.
        This is the setting actually take effective
        """
        if getattr(current_user, 'locale', None) is not None:
            return current_user.locale.code
        return 'zh_CN' if current_app.config['DEBUG'] else request.accept_languages.best_match(['zh_CN', 'en_US'])


def init_all(app):
    database = init_db(app)
    init_migrate(app, database)
    init_flask_security(app, database)
    init_admin_views(app, database)
    babel = init_babel(app)
    init_logging(app)
    # init_debug_toolbar(app)
    define_route_context(app, database, babel)
