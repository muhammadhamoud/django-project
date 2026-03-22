from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import CustomUser, UserProfile
from properties.models import Property


class UserAPITest(APITestCase):

    def setUp(self):

        self.user = CustomUser.objects.create_user(
            email="admin@test.com",
            password="12345678"
        )

        self.property = Property.objects.create(
            hotel_code="DEMO-1",
            resort_code="DEMO-R1"
        )

        self.user.profile.properties.add(self.property)

        # Login
        response = self.client.post(reverse("accounts:login"), {
            "email": "admin@test.com",
            "password": "12345678"
        })

        self.token = response.data["tokens"]["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    # -----------------------------
    # TEST: Get users
    # -----------------------------
    def test_get_users(self):

        url = reverse("accounts:user_list") + f"?property_id={self.property.id}"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    # -----------------------------
    # TEST: Create user
    # -----------------------------
    def test_create_user(self):

        url = reverse("accounts:user_list")

        data = {
            "email": "staff@test.com",
            "password": "12345678",
            "first_name": "Staff",
            "last_name": "User",
            "property_id": self.property.id
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)

    # -----------------------------
    # TEST: Forbidden access
    # -----------------------------
    def test_property_forbidden(self):

        url = reverse("accounts:user_list") + "?property_id=999"

        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)