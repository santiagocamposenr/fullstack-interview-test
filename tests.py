import unittest
from application import app, db
from create_creds import read_creds_file
import json

creds = read_creds_file()


class BasicTestCase(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{creds['postgres_user']}:{creds['postgres_password']}@localhost:5432/test_db"
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()
    # Testing routes

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Index', response.data)

    def test_branches(self):
        tester = app.test_client(self)
        response = tester.get('/branches', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Branches', response.data)

    def test_pullrequests(self):
        tester = app.test_client(self)
        response = tester.get('/pullrequests', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Pull Requests', response.data)

    def test_commits(self):
        tester = app.test_client(self)
        response = tester.get(
            '/branches/alfonsolzrg-add-instructions', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Commits', response.data)

    def test_create_pr(self):
        tester = app.test_client(self)
        response = tester.get('/pullrequest_form', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create a pull', response.data)

    # testing models
    # helper method
    def create_pullrequest(self, id, author, title, description, status, base):
        return self.app.post(
            '/create_pullrequest',
            data=dict(id=id, author=author, title=title,
                      description=description, status=status, base=base),
            follow_redirects=True
        )

    def test_create_pullrequest_fail(self):
        response = self.create_pullrequest(
            440713420, 'santiagocamposenr', 'Branch detail view added', 'Testing the update of the db', 'closed', 'master')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error', response.data)

    # Testing endpoints
    def test_api_branches(self):
        tester = app.test_client(self)
        response = tester.get('/api/branches')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['results'][0]['id'],
                         "alfonsolzrg-add-instructions")

    def test_api_branch_id(self):
        tester = app.test_client(self)
        response = tester.get('/api/branches/master')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['results'][0]['branch_id'],
                         "master")

    # def test_api_pullrequests(self):
    #     tester = app.test_client(self)
    #     response = tester.get('/api/pullrequests')
    #     data = json.loads(response.get_data())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data['results'][0]['base'],
    #                      "master")


if __name__ == '__main__':
    with app.app_context():
        unittest.main()
