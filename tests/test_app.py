import unittest
from app import create_app, db
from app.models import User
import os
import tempfile

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_steganography(self):
        # Create test image
        with tempfile.NamedTemporaryFile(suffix='.png') as temp_file:
            response = self.client.post('/encode', data={
                'image': (temp_file, 'test.png'),
                'message': 'Test message'
            }, follow_redirects=True)
            self.assertEqual(response.status_code, 200)