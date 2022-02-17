from urllib import response
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
import mock

from rest_framework.test import APITestCase

from server_app.models import phone_number, account


def login_user():

    user = User.objects.create_user("test_user", email="test_user@mail.com", password="test123")
    account_obj = account.objects.create(user=user, auth_id='tui7869', username=user.username)
    phone_num = phone_number.objects.create(number=1234567890, account=account_obj)
    return user, phone_num


class InboundSmsTestCase(APITestCase):

    # missing to parameter given 403 error
    def test_inbound_with_out_to(self):
        url = reverse("api_inbound")
        user, phone_num = login_user()

        self.client.force_authenticate(user)
        response = self.client.post(url, {
            "_from": 'this is testing from',
            "_text":'Hi this is testing text'
        }, format='multipart')
        self.assertEqual(403, response.status_code)

    # missing to parameter given 403 error
    def test_inbound_with_out_from(self):
        url = reverse("api_inbound")
        user, phone_num = login_user()

        self.client.force_authenticate(user)
        response = self.client.post(url, {
            "_to": 'this is testing to',
            "_text":'Hi this is testing text'
        }, format='multipart')
        self.assertEqual(403, response.status_code)

    # missing to parameter given 403 error
    def test_inbound_with_out_text(self):
        url = reverse("api_inbound")
        user, phone_num = login_user()

        self.client.force_authenticate(user)
        response = self.client.post(url, {
            "_from": 'this is testing from',
            "_to":'Hi this is testing to'
        }, format='multipart')
        self.assertEqual(403, response.status_code)        

    def test_inbound_sms_not_match_to_with_user_num(self):

        url = reverse("api_inbound")
        user, phone_num = login_user()

        self.client.force_authenticate(user)
        response = self.client.post(url, {
            "_to": 864769,
            "_text": "hi this is also testing text",
            "_from": "this is testing from",
        }, format='json')
        self.assertEqual(403, response.status_code)
        
    def test_inbound_sms_stop_in_text(self):

        url = reverse("api_inbound")
        user, phone_num = login_user()

        self.client.force_authenticate(user)
        response = self.client.post(url, {
            "_to": 864769,
            "_text": "hi STOP is also testing text",
            "_from": "this is testing from",
        }, format='json')
        self.assertEqual(403, response.status_code)        


class OutboundSmsTestCase(APITestCase):

    # missing to parameter given 403 error
    def test_outbound_with_out_to(self):
        url = reverse("api_outbound")
        user, phone_num = login_user()

        self.client.force_authenticate(user)
        response = self.client.post(url, {
            "from": 'this is testing from',
            "text":'Hi this is testing text'
        }, format='multipart')
        self.assertEqual(403, response.status_code)

    # missing to parameter given 403 error
    def test_outbound_with_out_from(self):
        url = reverse("api_outbound")
        user, phone_num = login_user()

        self.client.force_authenticate(user)
        response = self.client.post(url, {
            "to": 'this is testing to',
            "text":'Hi this is testing text'
        }, format='multipart')
        self.assertEqual(403, response.status_code)

    # missing to parameter given 403 error
    def test_outbound_with_out_text(self):
        url = reverse("api_outbound")
        user, phone_num = login_user()

        self.client.force_authenticate(user)
        response = self.client.post(url, {
            "from": 'this is testing from',
            "to":'Hi this is testing to'
        }, format='multipart')
        self.assertEqual(403, response.status_code)    

    def test_outbound_sms_not_match_from_with_user_num(self):

        url = reverse("api_inbound")
        user, phone_num = login_user()

        self.client.force_authenticate(user)
        response = self.client.post(url, {
            "_to": 864769,
            "_text": "hi this is also testing text",
            "_from": 98876568,
        }, format='json')
        self.assertEqual(403, response.status_code)