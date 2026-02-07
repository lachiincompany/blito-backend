from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import CustomUser, Profile


def reverse_any(names, args=None, kwargs=None):
    args = args or []
    kwargs = kwargs or {}
    last_err = None
    for name in names:
        try:
            return reverse(name, args=args, kwargs=kwargs)
        except Exception as e:
            last_err = e
    raise last_err



SEND_EMAIL_PATCH_PATHS = [
    "accounts.api.v1.serializers.send_verification_email",
    "accounts.serializers.send_verification_email",
    "accounts.api.serializers.send_verification_email",
]


class AccountsAPITests(APITestCase):
    def make_user(self, phone="09123456789", password="Abcdef123!", full_name="Test User", email="t@example.com", verified=True):
        user = CustomUser.objects.create_user(
            phone=phone,
            password=password,
            full_name=full_name,
            email=email,
        )
        user.is_verified = verified
        user.save(update_fields=["is_verified"])
        Profile.objects.get_or_create(
            user=user,
            defaults={"first_name": "Test", "last_name": "User"},
        )
        return user

    def _patch_send_email(self):
        """
        Try patching send_verification_email from known paths.
        Returns a context manager.
        """
        last_err = None
        for p in SEND_EMAIL_PATCH_PATHS:
            try:
                return patch(p)
            except Exception as e:
                last_err = e
        return None

    def test_register_success(self):
        url = reverse_any(["accounts:register", "register", "auth-register"])
        payload = {
            "phone": "09111111111",
            "full_name": "Ali Test",
            "email": "ali@test.com",
            "password1": "Abcdef123!",
            "password2": "Abcdef123!",
        }

        cm = self._patch_send_email()
        if cm:
            with cm as mocked:
                res = self.client.post(url, payload, format="json")
        else:
            res = self.client.post(url, payload, format="json")

        self.assertIn(res.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
        self.assertTrue(CustomUser.objects.filter(phone="09111111111").exists())

    def test_register_password_mismatch_should_fail(self):
        url = reverse_any(["accounts:register", "register", "auth-register"])
        payload = {
            "phone": "09122222222",
            "full_name": "Mismatch Test",
            "email": "mismatch@test.com",
            "password1": "Abcdef123!",
            "password2": "DIFFERENT123!",
        }

        cm = self._patch_send_email()
        if cm:
            with cm:
                res = self.client.post(url, payload, format="json")
        else:
            res = self.client.post(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_verified_success(self):
        self.make_user(phone="09133333333", password="Abcdef123!", verified=True)

        url = reverse_any(["accounts:token_obtain_pair", "accounts:login", "token_obtain_pair", "login"])
        res = self.client.post(url, {"phone": "09133333333", "password": "Abcdef123!"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    def test_login_unverified_should_fail(self):
        self.make_user(phone="09144444444", password="Abcdef123!", verified=False)

        url = reverse_any(["accounts:token_obtain_pair", "accounts:login", "token_obtain_pair", "login"])
        res = self.client.post(url, {"phone": "09144444444", "password": "Abcdef123!"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_success(self):
        user = self.make_user(phone="09166666666", password="Abcdef123!", verified=True)
        self.client.force_authenticate(user=user)

        url = reverse_any(["accounts:change_password", "change_password", "accounts:password-change"])
        res = self.client.put(url, {"old_password": "Abcdef123!", "new_password": "Newpass123!"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_logout_authenticated_success(self):
        user = self.make_user(phone="09188888888", password="Abcdef123!", verified=True)
        self.client.force_authenticate(user=user)

        url = reverse_any(["accounts:logout", "logout"])
        res = self.client.post(url, {}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
