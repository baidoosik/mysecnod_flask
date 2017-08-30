import unittest
from app import create_app, db
from app.models import User


class UserModelTestCase(unittest.TestCase):
    # test 시작할 때 셋팅되는 부분.
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    # test 끝날 때 실행되는 부분
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.passoword is not None)

    def test_no_passwor_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.passoword

    def test_password_verification(self):
        u =User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('cow'))

    def test_password_salts_are_random(self):
        u= User(password='cat')
        u2= User(password='cat')
        self.assertFalse(u.password_hash==u2.password_hash)

