from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from visionbuilder.models import Page

class VisionBuilderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a test user.
        self.user = User.objects.create_user(username='testuser@test.com', password='testtest22&&')
        self.user.save()

        # Create a test page.
        self.page = Page.objects.create(user=self.user, name='Test Page', content={"key": "value"})
        self.page.save()

    def test_create_user(self):
        # Test creating a new user.
        new_user_data = {
            'username': 'newuser@test.com',
            'password': 'testtest22&&'
        }
        response = self.client.post('/api/v1/users/', new_user_data)
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        login_data = {
            'username': 'testuser@test.com',
            'password': 'testtest22&&'
        }
        response = self.client.post('/api/v1/token/login/', login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', response.data)

    def test_logout_user(self):
            # Login first to get the auth token.
            login_data = {
                'username': 'testuser@test.com',
                'password': 'testtest22&&'
            }
            login_response = self.client.post('/api/v1/token/login/', login_data)
            token = login_response.data['auth_token']

            # Test logging out the user.
            self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
            response = self.client.post('/api/v1/token/logout/')
            self.assertEqual(response.status_code, 204)

    def test_create_page(self):
        # Login first to get the auth token.
        login_data = {
            'username': 'testuser@test.com',
            'password': 'testtest22&&'
        }
        login_response = self.client.post('/api/v1/token/login/', login_data)
        token = login_response.data['auth_token']

        # Test creating a new page.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        new_page_data = {
            'name': 'New Page',
            'content': {"key": "value"}
        }
        response = self.client.post(reverse('pages_list_create'), new_page_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.data)

    def test_delete_page(self):
        # Login first to get the auth token.
        login_data = {
            'username': 'testuser@test.com',
            'password': 'testtest22&&'
        }
        login_response = self.client.post('/api/v1/token/login/', login_data)
        token = login_response.data['auth_token']

        # Test deleting a page.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.delete(reverse('page_retrieve_update', args=[self.page.id]))
        self.assertEqual(response.status_code, 204)

    def test_display_pages(self):
        # Login first to get the auth token.
        login_data = {
            'username': 'testuser@test.com',
            'password': 'testtest22&&'
        }
        login_response = self.client.post('/api/v1/token/login/', login_data)
        token = login_response.data['auth_token']

        # Test displaying pages for the authenticated user.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.get(reverse('pages_list_create'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Page')
        self.assertEqual(response.data[0]['content'], {"key": "value"})

    def test_make_page_public(self):
        # Login first to get the auth token.
        login_data = {
            'username': 'testuser@test.com',
            'password': 'testtest22&&'
        }
        login_response = self.client.post('/api/v1/token/login/', login_data)
        token = login_response.data['auth_token']

        # Test making a page public.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        update_data = {
            'public': True
        }
        response = self.client.put(reverse('page_retrieve_update', args=[self.page.id]), update_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['public'])

    def test_get_page_with_id(self):
        # Login first to get the auth token.
        login_data = {
            'username': 'testuser@test.com',
            'password': 'testtest22&&'
        }
        login_response = self.client.post('/api/v1/token/login/', login_data)
        token = login_response.data['auth_token']

        # Test getting a specific page by ID.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        response = self.client.get(reverse('page_retrieve_update', args=[self.page.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Page')
        self.assertEqual(response.data['content'], {"key": "value"})

    def test_get_public_pages(self):
         # Make the test page public.
        self.page.public = True
        self.page.save()

        # Test getting public pages without authentication.
        self.client.credentials()  # Clear any existing credentials.
        response = self.client.get(reverse('public_pages'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Page')
        self.assertEqual(response.data[0]['user'], self.user.username)