from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

VALID = {
    "username": "newuser",
    "first_name": "Ada",
    "last_name": "Okello",
    "email": "ada@example.com",
    "password1": "S0me-long-pass!",
    "password2": "S0me-long-pass!",
}


class SignUpTests(TestCase):
    def test_logged_out_sees_form(self):
        response = self.client.get(reverse("sign_up"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "first_name")

    def test_valid_signup_creates_user_and_logs_in(self):
        response = self.client.post(reverse("sign_up"), VALID)
        self.assertRedirects(response, reverse("dashboard"))
        user = User.objects.get(username="newuser")
        self.assertEqual(user.email, "ada@example.com")
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_password_mismatch_creates_no_user(self):
        response = self.client.post(reverse("sign_up"), {**VALID, "password2": "different"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_duplicate_username_shows_error(self):
        User.objects.create_user("newuser", password="x")
        response = self.client.post(reverse("sign_up"), VALID)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already exists")

    def test_email_is_required(self):
        response = self.client.post(reverse("sign_up"), {**VALID, "email": ""})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newuser").exists())


class AccessRuleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("member", password="pw-12345-xyz")

    def test_logged_in_is_redirected_from_sign_up(self):
        self.client.force_login(self.user)
        self.assertRedirects(self.client.get(reverse("sign_up")), reverse("dashboard"))

    def test_logged_in_is_redirected_from_login(self):
        self.client.force_login(self.user)
        self.assertRedirects(self.client.get(reverse("login")), reverse("dashboard"))

    def test_logged_out_is_sent_to_login(self):
        response = self.client.get("/clients/")
        self.assertRedirects(response, "/login/?next=/clients/")

    def test_login_page_links_to_sign_up_when_logged_out(self):
        self.assertContains(self.client.get(reverse("login")), reverse("sign_up"))

    def test_non_staff_cannot_use_admin(self):
        self.client.force_login(self.user)
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_overview_has_no_sign_up_link(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "sign_up")
        self.assertNotContains(response, "Create an account")
