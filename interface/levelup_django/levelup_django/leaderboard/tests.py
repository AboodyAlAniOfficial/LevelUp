from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Follower

class FollowerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")
        self.client.force_authenticate(user=self.user1)  # Simulate login

    def test_search_users(self):
        response = self.client.get("/api/search-users/?q=user")
        self.assertEqual(response.status_code, 200)
        self.assertIn("user1", [u["username"] for u in response.json()["users"]])
        self.assertIn("user2", [u["username"] for u in response.json()["users"]])

    def test_follow_user(self):
        response = self.client.post("/api/follow-user/", {"user_id": self.user2.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Follower.objects.filter(follower=self.user1, following=self.user2).exists())

    def test_follow_self(self):
        response = self.client.post("/api/follow-user/", {"user_id": self.user1.id})
        self.assertEqual(response.status_code, 400)
        self.assertIn("You cannot follow yourself", response.json()["error"])

    def test_unfollow_user(self):
        Follower.objects.create(follower=self.user1, following=self.user2)  # Manually follow first
        response = self.client.post("/api/unfollow-user/", {"user_id": self.user2.id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Follower.objects.filter(follower=self.user1, following=self.user2).exists())

    def test_unfollow_not_following(self):
        response = self.client.post("/api/unfollow-user/", {"user_id": self.user2.id})
        self.assertEqual(response.status_code, 200)  # Should not error out
