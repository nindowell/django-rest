# from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from .models import Post

# Create your tests here.


class PostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = APIClient()
        self.client.login(username='testuser', password='12345')
        self.post_data = {'title': 'Test Post', 'content': 'This is content for test post.'}
        self.posts = [
            Post.objects.create(author=self.user, title=f'Post {i}', content=f'This is post number {i}.')
            for i in range(15)
        ]

    def test_create_post(self):
        url = reverse('post_list_create')
        response = self.client.post(url, self.post_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 16)
        self.assertEqual(Post.objects.last().title, self.post_data['title'])

    def test_list_posts(self):
        url = reverse('post_list_create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.data['count'], 15)

    def test_retrieve_post(self):
        url = reverse('post_detail', kwargs={'pk': self.posts[0].id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.posts[0].title)

    def test_update_post(self):
        url = reverse('post_detail', kwargs={'pk': self.posts[0].id})
        updated_data = {'title': 'Updated Post', 'content': 'Content update post.'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.posts[0].refresh_from_db()
        self.assertEqual(self.posts[0].title, updated_data['title'])

    def test_delete_post(self):
        url = reverse('post_detail', kwargs={'pk': self.posts[0].id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.count(), 14)
