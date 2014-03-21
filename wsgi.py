# -*- coding: utf-8 -*-

from app.main import create_app

application = None

# Create application object for debugging or production.
# http://pythonhosted.org/Flask-SQLAlchemy/contexts.html
if __name__ == '__main__':
    from flask.ext.script import Manager
    from flask.ext.assets import ManageAssets
    from flask.ext.migrate import Migrate, MigrateCommand
    from app.shared.models import db
    from app.assets import assets_env
    from app.util import GenerateSitemap

    application = create_app(debug=True)
    application.test_request_context().push()

    # This 'migrate' instance is required by MigrateCommand.
    migrate = Migrate(application, db)
    manager = Manager(application)
    manager.add_command('db', MigrateCommand)
    manager.add_command('assets', ManageAssets(assets_env))
    manager.add_command('sitemap', GenerateSitemap(application.static_folder))
    manager.run()
else:
    application = create_app(debug=False)
