import unittest
from application import app


class BasicTestCase(unittest.TestCase):

    # Testing routes
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data, b'Index' in response.data)

    def test_branches(self):
        tester = app.test_client(self)
        response = tester.get('/branches', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data, b'branches' in response.data)

    def test_pullrequests(self):
        tester = app.test_client(self)
        response = tester.get('/pullrequests', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data, b'Pull Requests' in response.data)

    def test_commits(self):
        tester = app.test_client(self)
        response = tester.get(
            '/branches/alfonsolzrg-add-instructions', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data, b'Commits' in response.data)

    def test_create_pr(self):
        tester = app.test_client(self)
        response = tester.get('/pullrequest_form', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data, b'Create a pull' in response.data)


if __name__ == '__main__':
    unittest.main()
