from django.test  import  TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from organisation.models import Organisation

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_USER = reverse('auth:signup')
LOGIN_URL = reverse('auth:signin')

print(CREATE_USER_USER)

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'name':'example',
            'email':'test@example.com',
            'password':'password..123',
            'lastName':'lstname',
            'firstName':'firstname',
            'phone':'0901234566'
        }
        res = self.client.post(CREATE_USER_USER,payload)


        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email = payload['email'])
        org = Organisation.objects.filter(name = f'{user.firstName}`s organsation')
        tt = bool(len(org))
        self.assertTrue(tt)
        self.assertTrue(user.check_password(payload['password']))
        self.assertIn('accessToken',res.data.data)
        self.assertNotIn('password',res.data)

    def test_user_login(self):
        payload = {
            'email':'test@example.com',
            'password':'password..123',
            'lastName':'lstname',
            'firstName':'firstname',
            'phone':'0901234566'
        }
        res = self.client.post(CREATE_USER_USER,payload)
        login_payload ={
            'password':'password..123',
            'email':'test@example.com',
        }
        res = self.client.post(LOGIN_URL,login_payload)
        self.assertIn('accessToken',res.data.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)


    def test_user_login_with_incomplete_field(self):
        payload = [{
            'email':'',
            'password':'password..123',
            'lastName':'lstname',
            'firstName':'firstname',
            'phone':'0901234566'
        },{
            'email':'exampl@gamil.com',
            'password':'',
            'lastName':'lstname',
            'firstName':'firstname',
            'phone':'0901234566'
        },{
            'email':'',
            'password':'password..123',
            'lastName':'',
            'firstName':'firstname',
            'phone':'0901234566'
        },{
            'email':'exampl@gamil.com',
            'password':'password..123',
            'lastName':'lstname',
            'firstName':'',
            'phone':'0901234566'
        },{
            'email':'exampl@gamil.com',
            'password':'password..123',
            'lastName':'lstname',
            'firstName':'firstname',
            'phone':''
        },]

        for pay in payload:
            res = self.client.post(CREATE_USER_USER,pay)
            self.assertEqual(res.status_code,status.HTTP_422_UNPROCESSABLE_ENTITY)

    def test_user_login_that_exist(self):
        payload = {
            'email':'test@example.com',
            'password':'password..123',
            'lastName':'lstname',
            'firstName':'firstname',
            'phone':'0901234566'
        }
        res = self.client.post(CREATE_USER_USER,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        restwo = self.client.post(CREATE_USER_USER,payload)
        self.assertEqual(restwo.status_code,status.HTTP_422_UNPROCESSABLE_ENTITY)


