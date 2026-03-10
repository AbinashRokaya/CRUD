from django.test import TestCase
from django.urls import reverse

class NotesTestCase(TestCase):

    def test_notes_can_be_created(self):
        # Send POST request to create a new note
        response = self.client.post(reverse('notes:add'), {
            'title': 'Django Course',
            'description': 'Complete course with urls, templates, models, etc'
        })

        # Check if the request redirects after successful creation
        self.assertEqual(response.status_code, 302)

        # Follow the redirect and check if the note appears in the response
        response = self.client.get(response.url)
        self.assertContains(response, 'Django Course')

        print("PASS: test_notes_can_be_created - Abinash Rokaya | Roll: 4")


    def test_error_occurs_if_description_is_less_than_10_chars_long(self):
        # Send POST request with invalid description (less than 10 characters)
        response = self.client.post(reverse('notes:add'), {
            'title': 'Django Course',
            'description': 'dj'
        })

        # The form should return to the page with validation errors
        self.assertEqual(response.status_code, 200)

        # Check if the correct validation error message appears
        self.assertContains(
            response, 'Description must be at least 10 characters long'
        )

        print("PASS: test_error_occurs_if_description_is_less_than_10_chars_long - Abinash Rokaya | Roll: 4")