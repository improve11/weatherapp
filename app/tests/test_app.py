import unittest
from app import create_app, db
from app.models import WeatherHistory

class WeatherAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_index_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Get Weather', response.data)

    def test_get_weather(self):
        response = self.client.post('/', data={'city': 'Berlin'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Weather in', response.data)

    def test_history_page_loads(self):
        response = self.client.get('/history')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'History', response.data)

    def test_search_history(self):
        with self.app.app_context():
            history = WeatherHistory(city='Berlin')
            db.session.add(history)
            db.session.commit()

        response = self.client.get('/history')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Last searched city: Berlin', response.data)

    def test_api_history(self):
        with self.app.app_context():
            history = WeatherHistory(city='Berlin')
            db.session.add(history)
            db.session.commit()

        response = self.client.get('/api/history')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Berlin', response.data)

if __name__ == '__main__':
    unittest.main()
