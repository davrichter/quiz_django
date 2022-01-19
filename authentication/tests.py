from django.test import TestCase
from django.urls import reverse


class UserIndexViewTests(TestCase):
    def test_create_user(self):
        username = 'test'
        self.client.post(reverse('CreateUser'), {
            'username': username,
            'password': '123',
            'first_name': '',
            'last_name': ''
        })
        response = self.client.get(reverse('ViewUser', args=[1]))

        self.assertContains(response, username)

    def test_create_user_first_name(self):
        username = 'test2'
        first_name = 'Tom'
        self.client.post(reverse('CreateUser'), {
            'username': username,
            'password': '123',
            'first_name': first_name,
            'last_name': ''
        })
        response = self.client.get(reverse('ViewUser', args=[1]))

        self.assertContains(response, first_name)

    def test_create_user_last_name(self):
        username = 'test3'
        last_name = 'Smith'
        self.client.post(reverse('CreateUser'), {
            'username': username,
            'password': '123',
            'first_name': '',
            'last_name': last_name
        })
        response = self.client.get(reverse('ViewUser', args=[1]))

        self.assertContains(response, last_name)
