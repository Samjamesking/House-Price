from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class PredictionAppTests(TestCase):
    
    def test_landing_page_loads(self):
        """
        Verify that the landing page renders with status 200.
        """
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ames Valuer AI")

    def test_predict_page_requires_login(self):
        """
        Predict evaluation endpoint should redirect to login if user is unauthenticated.
        """
        response = self.client.get(reverse('predict'))
        self.assertEqual(response.status_code, 302) # Redirect to login
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_history_page_requires_login(self):
        """
        Prediction history list page should redirect to login if user is unauthenticated.
        """
        response = self.client.get(reverse('prediction_history'))
        self.assertEqual(response.status_code, 302) # Redirect to login
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_analytics_page_requires_login(self):
        """
        Analytics page should redirect to login if user is unauthenticated.
        """
        response = self.client.get(reverse('analytics_dashboard'))
        self.assertEqual(response.status_code, 302) # Redirect to login
        self.assertTrue(response.url.startswith(reverse('login')))
