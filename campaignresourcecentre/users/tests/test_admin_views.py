# from unittest import mock
#
# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.urls import reverse
#
# from campaignresourcecentre.notifications import FakeNotifications
#
#
# class PasswordResetTestCase(TestCase):
#     """Test the overridden password reset view."""
#
#     def test_password_reset_govuk_notification(self):
#         """Test that the password reset page sends the notification using the
#         GOV.UK Notify service"""
#         User = get_user_model()
#         user = User.objects.create_user(
#             email="rich@test.com",
#             first_name="Rich",
#             password="testing",
#             username="rich",
#         )
#
#         with mock.patch(
#             "campaignresourcecentre.users.admin_forms.gov_notify_factory",
#             FakeNotifications(),
#         ) as mock_notifications:
#             self.client.post(
#                 reverse("wagtailadmin_password_reset"), {"email": user.email}
#             )
#             self.assertIn(user.email, mock_notifications)
#             self.assertEqual("Rich", mock_notifications[user.email]["first_name"])
#             self.assertIn(
#                 "/crc-admin/password_reset/confirm/",
#                 mock_notifications[user.email]["reset_link"],
#             )
