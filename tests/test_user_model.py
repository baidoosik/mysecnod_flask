import unittest
from app import create_app, db
from app.models import User,Role,Permission,AnonymousUser


class UserModelTestCase(unittest.TestCase):
    # test 시작할 때 셋팅되는 부분.
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()


    # test 끝날 때 실행되는 부분
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

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

    def test_roles_and_permissions(self):
        Role.insert_roles()
        u =User(email='john@example.com',password='cat')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anyomous_user(self):
        u=AnonymousUser()
        self.assertFalse(u.can(Permission.COMMENT))
