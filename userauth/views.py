
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from userauth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate





# Serializers
from userauth.serializer import RegisterSerializer,UserLoginSerializer




class MyTokenObtainPairView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        password = request.data['password']
        user = authenticate(request=request,email=email,password=password)
        if user:
            token = RefreshToken.for_user(user)
            return Response({
                "status": "success",
                "message": "Login successful",
                "data": {
                      "accessToken":str(token.access_token),
                    "user": {
                         "userId": user.userId,
                         "firstName": user.firstName,
                         "lastName": user.lastName,
                         "email": user.email,
                         "phone": user.phone,
                         }
                    }
                },status=status.HTTP_200_OK)
        return Response({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
            },status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)




class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


    def post(self, request, *args, **kwargs):
        userexist = User.objects.filter(email=request.data['email'])
        if userexist:
               return Response({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 422
            },status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if not request.data['email'] or not request.data['password'] or not request.data['firstName'] or not request.data['lastName'] or not request.data['phone']:
            return Response({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 422
            },status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        statu =  self.create(request, *args, **kwargs)
        if statu.status_code == 201:
            user = User.objects.get(email = request.data['email'])
            token = RefreshToken.for_user(user)
            return Response({
                "status": "success",
                "message": "Registration successful",
                "data": {
                      "accessToken":str(token.access_token),
                    "user": {
                         "userId": user.userId,
                         "firstName": user.firstName,
                         "lastName": user.lastName,
                         "email": user.email,
                         "phone": user.phone,
                         }
                    }
                },status=status.HTTP_201_CREATED)





        return Response({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": 422
            },status=status.HTTP_400_BAD_REQUEST)



