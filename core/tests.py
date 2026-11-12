# Automated tests for sign-up and for who is allowed to see which page.
#
# Plain English: a test is a small script that uses the site like a visitor and checks
# the result, so we notice quickly if a change breaks something. Run them all with
# `python manage.py test`. Technical: Django's TestCase gives every test a fresh, empty
# temporary database and a fake browser available as self.client.

# Plain English: the login accounts table, used to create users for the tests.
from django.contrib.auth.models import User
# TestCase is the base class that sets up the temporary database and fake browser.
from django.test import TestCase
# Plain English: turns a route name into its address, so tests do not hard-code URLs.
from django.urls import reverse

# Plain English: one complete, correct sign-up form. Technical: tests that need a bad
# form copy it and change one value ({**VALID, "email": ""}), so each test shows exactly
# what is wrong and everything else stays valid.
VALID = {
    "username": "newuser",
    "first_name": "Ada",
    "last_name": "Okello",
    "email": "ada@example.com",
    "password1": "S0me-long-pass!",
    "password2": "S0me-long-pass!",
}


# Covers the sign-up page: the happy path and the ways it can fail.
class SignUpTests(TestCase):
    def test_logged_out_sees_form(self):
        # The page opens (status 200 = OK) and shows the extra fields we added.
        response = self.client.get(reverse("sign_up"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "first_name")

    def test_valid_signup_creates_user_and_logs_in(self):
        # Plain English: a correct form creates the account, saves the email and logs the
        # person in. Technical: the session key _auth_user_id is how Django remembers who is in.
        response = self.client.post(reverse("sign_up"), VALID)
        self.assertRedirects(response, reverse("dashboard"))
        user = User.objects.get(username="newuser")
        self.assertEqual(user.email, "ada@example.com")
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_password_mismatch_creates_no_user(self):
        # Status 200 means the form was shown again (with errors) instead of redirecting.
        response = self.client.post(reverse("sign_up"), {**VALID, "password2": "different"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_duplicate_username_shows_error(self):
        # Create the clashing user first, then try to sign up with the same username.
        User.objects.create_user("newuser", password="x")
        response = self.client.post(reverse("sign_up"), VALID)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already exists")

    def test_email_is_required(self):
        # Proves the extra email field we declared in core/forms.py really is required.
        response = self.client.post(reverse("sign_up"), {**VALID, "email": ""})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newuser").exists())


# Covers the access rules: who may see which page, and who gets redirected.
class AccessRuleTests(TestCase):
    # Plain English: setUp runs before every test in this class, so each starts with
    # one ordinary (non-staff) member ready to use.
    def setUp(self):
        self.user = User.objects.create_user("member", password="pw-12345-xyz")

    # Plain English: force_login is a shortcut that logs the fake browser in without
    # typing a password. Technical: it writes the session directly, skipping the login form.
    def test_logged_in_is_redirected_from_sign_up(self):
        self.client.force_login(self.user)
        self.assertRedirects(self.client.get(reverse("sign_up")), reverse("dashboard"))

    def test_logged_in_is_redirected_from_login(self):
        # This is what redirect_authenticated_user=True in realestate/urls.py does.
        self.client.force_login(self.user)
        self.assertRedirects(self.client.get(reverse("login")), reverse("dashboard"))

    def test_logged_out_is_sent_to_login(self):
        # @login_required sends visitors to /login/ and remembers the page they wanted (?next=).
        response = self.client.get("/clients/")
        self.assertRedirects(response, "/login/?next=/clients/")

    def test_login_page_links_to_sign_up_when_logged_out(self):
        self.assertContains(self.client.get(reverse("login")), reverse("sign_up"))

    def test_non_staff_cannot_use_admin(self):
        # Status 302 is a redirect: a normal member is bounced to the admin login page.
        self.client.force_login(self.user)
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response["Location"])

    def test_overview_has_no_sign_up_link(self):
        # Once you are in, the Overview must not offer to create another account.
        self.client.force_login(self.user)
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "sign_up")
        self.assertNotContains(response, "Create an account")
