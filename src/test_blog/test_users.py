import unittest
import json

from ..app import create_app, db


class UsersTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.user = {
            'name': 'ds997',
            'email': 'ds997@njit.edu',
            'password': 'passw0rd!'
        }

        with self.app.app_context():
            # create all tables
            db.create_all()

    " test for user creation with valid credentials "

    def test_user_creation(self):
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        json_data = json.loads(res.data)
        self.assertTrue(json_data.get('jwt_token'))
        self.assertEqual(res.status_code, 201)

    " test user creation with already existing email"

    def test_user_creation_with_existing_email(self):
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('error'))

    " test user creation with no password"
    def test_user_creation_with_no_password(self):

        user1 = {
            'name': 'ds997',
            'email': 'ds997@njit.edu',
        }
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('password'))


if __name__ == '__main__':
    unittest.main()
