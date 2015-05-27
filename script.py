"""Manger script."""
import os
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db, AuthUser

manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    """make variables available in shell."""
    return dict(
        app=app,
        db=db,
        AuthUser=AuthUser
    )


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
