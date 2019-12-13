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

    " test user creation with no email "

    def test_user_creation_with_no_email(self):
        user1 = {
            'name': 'ds997',
            'password': 'ds997@njit.edu',
        }
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('email'))

    "test user creation with empty request"

    def test_user_creation_with_empty_request(self):
        user1 = {}
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'}, data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_user_login(self):
        """ User Login Tests """
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        json_data = json.loads(res.data)
        self.assertTrue(json_data.get('jwt_token'))
        self.assertEqual(res.status_code, 200)

    def test_user_login_with_invalid_password(self):
        """ User Login Tests with invalid credentials """
        user1 = {
            'password': 'ds997',
            'email': 'ds997@njit.edu',
        }
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertFalse(json_data.get('jwt_token'))
        self.assertEqual(json_data.get('error'), 'invalid credentials')
        self.assertEqual(res.status_code, 400)

    def test_user_login_with_invalid_email(self):
        """ User Login Tests with invalid credentials """
        user1 = {
            'password': 'passw0rd!',
            'email': 'ds997@njit.edu',
        }
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/users/login', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertFalse(json_data.get('jwt_token'))
        self.assertEqual(json_data.get('error'), 'invalid credentials')
        self.assertEqual(res.status_code, 400)

    def test_user_get_me(self):
        """ Test User Get Me """
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().get('/api/v1/users/me',
                                headers={'Content-Type': 'application/json', 'api-token': api_token})
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('email'), 'ds997@njit.edu')
        self.assertEqual(json_data.get('name'), 'ds997')

    def test_user_update_me(self):
        """ Test User Update Me """
        user1 = {
            'name': 'new name'
        }
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().put('/api/v1/users/me',
                                headers={'Content-Type': 'application/json', 'api-token': api_token},
                                data=json.dumps(user1))
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('name'), 'new name')

    def test_delete_user(self):
        """ Test User Delete """
        res = self.client().post('/api/v1/users/', headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)
        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().delete('/api/v1/users/me',
                                   headers={'Content-Type': 'application/json', 'api-token': api_token})
        self.assertEqual(res.status_code, 204)

    def tearDown(self):
        """
        Tear Down
        """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
