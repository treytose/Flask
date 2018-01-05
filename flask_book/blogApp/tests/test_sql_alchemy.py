import unittest
from app import create_app, db
from app.models import User, Role
from flask import current_app

class SQLAlchemyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        admin_role = Role(name='Admin')
        admin_user = User(username='Trey', role=admin_role)
        db.session.add(admin_role)
        db.session.add(admin_user)
        db.session.commit()

    def tearDown(self):
        #db.session.remove() #NOTE: causes test_runner to fail, dropping tables before other tests are run.
        #db.drop_all()
        self.app_context.pop()

    def test_user_table_exists(self):
        self.assertTrue(User.query.filter_by(username='Trey').first())
