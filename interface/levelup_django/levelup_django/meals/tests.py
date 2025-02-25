from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Meal

class MealsTestCase(TestCase):
    def setUp(self):
        # Set up the test client and create a test user.
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Use reverse() to generate URL based on your URL names
        self.log_meal_url = reverse('meals:log_meal')
        self.daily_calories_url = reverse('meals:daily_calories')

    def test_log_meal(self):
        """
        Test the log_meal endpoint by sending a POST request.
        """
        payload = {
            "user_id": self.user.id,
            "meal_name": "Test Meal",
            "ingredients": [
                {"name": "apple", "weight": 150},
                {"name": "chicken breast", "weight": 200}
            ]
        }
        response = self.client.post(self.log_meal_url, payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Meal logged successfully", response.json().get("message", ""))

    def test_daily_calories(self):
        """
        Test the daily_calories endpoint by:
          1. Creating a meal directly.
          2. Retrieving total calories for the day.
        """
        # Create a Meal directly in the database
        Meal.objects.create(
            user=self.user,
            meal_name="Breakfast",
            calories=300,
            macronutrients={"fats": 10, "carbs": 40, "proteins": 20},
            ingredients=[{"name": "banana", "weight": 100}],
        )
        # Now, call the daily_calories endpoint
        response = self.client.get(self.daily_calories_url + f"?user_id={self.user.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("total_calories"), 300)
