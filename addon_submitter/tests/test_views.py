# coding: utf-8
# Author: Roman Miroshnychenko aka Roman V.M.
# E-mail: roman1972@gmail.com

import os
from io import BytesIO
from django.conf import settings
from django.shortcuts import reverse
from django.test import TestCase


class IndexViewTestCase(TestCase):
    def test_index_view_get(self):
        resp = self.client.get(reverse('index'))
        self.assertContains(resp, 'Submit Kodi Addon')

    def test_index_view_post_valid(self):
        zip_path = os.path.join(settings.BASE_DIR, 'test_data',
                                'plugin.video.example-2.2.0.zip')
        with open(zip_path, 'rb') as fo:
            data = {
                'author': 'John Doe',
                'author_email': 'jdoe@example.com',
                'github_username': 'jdoe',
                'addon_description': 'My cool addon',
                'git_repo': 'repo-plugins',
                'git_branch': 'leia',
                'zipped_addon': fo,
            }
            resp = self.client.post(reverse('index'), data)
            self.assertRedirects(resp, reverse('confirmation'))

    def test_index_view_post_invalid_zip(self):
        data = {
            'author': 'John Doe',
            'author_email': 'jdoe@example.com',
            'github_username': 'jdoe',
            'addon_description': 'My cool addon',
            'git_repo': 'repo-plugins',
            'git_branch': 'leia',
            'zipped_addon': BytesIO(b'foobar'),
        }
        resp = self.client.post(reverse('index'), data)
        self.assertTrue(resp.context['form'].errors)


class ConfirmationViewTestCase(TestCase):
    def test_confirmation_view(self):
        resp = self.client.get(reverse('confirmation'))
        self.assertContains(resp, 'Addon Has Been Submitted')
