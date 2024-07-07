
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from userauth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q


# Serializers
from userauth.serializer import UserSerializer
from organisation.serializer import OrgSerializer
from organisation.models  import Organisation



class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'userId'

    def get_queryset(self):
        userId = self.kwargs['userId']
        print(userId)
        try:
            oid = int(userId)
        except:
            oid = userId
        if type(oid) ==int:
            queryset = User.objects.filter(
            Q(userId=oid) |
            Q(pk=oid))
        else:
            queryset = User.objects.filter(userId=oid)

        return queryset

    def get(self, request, *args, **kwargs):


        user = self.get_queryset()
        if user:
            print(user)
            return Response({
                "status": "success",
                "message": "<message>",
                "data": {

                         "userId": user[0].userId,
                         "firstName": user[0].firstName,
                         "lastName": user[0].lastName,
                         "email": user[0].email,
                         "phone": user[0].phone,

                    }
                },status=status.HTTP_200_OK)

        return Response({
                "status": "error",
                "message": "invalid id",
                },status=status.HTTP_400_BAD_REQUEST)



class Orglistview(generics.ListCreateAPIView):
    queryset = Organisation.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes =(JWTAuthentication,)
    serializer_class = OrgSerializer

    def get(self, request, *args, **kwargs):
        orgs = Organisation.objects.filter(user__in=[request.user,]).values()


        if orgs:
            print(orgs)
            return Response({
                "status": "success",
                "message": "here are your organisations",
                "data": {"organisations": orgs

                    }
                },status=status.HTTP_200_OK)

        else:
            return Response({
                 "status": "success",
                 "message": "you are in no organisation",
                },status=status.HTTP_204_NO_CONTENT)



        return Response({
                "status": "error",
                "message": "invalid id",
                },status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        org = Organisation.objects.create(
            name=request.data['name'],
            description=request.data['description'],
        )
        org.save()
        request.user.organisation.add(org)

        return Response({
            "status": "success",
            "message": "<message>",
            "data": {
                "orgId": org.orgId,
                "name": org.name,
                "description": org.description,
                }
            })








class OrgDetailView(generics.RetrieveAPIView):
    serializer_class = OrgSerializer
    # queryset = Organisation.objects.all()
    # lookup_field ='orgId'

    def get_queryset(self):
        orgId = self.kwargs['orgid']
        try:
            oid = int(orgId)
        except:
            oid = orgId
        if type(oid) ==int:
            queryset = Organisation.objects.filter(
            Q(orgId=oid) |
            Q(pk=oid))
        else:
            queryset = Organisation.objects.filter(orgId=oid)


        return queryset
    def get(self, request, *args, **kwargs):
        user = self.get_queryset()
        print(user)
        if user:
            print(user)
            return Response({
                "status": "success",
                "message": "<message>",
                "data": {

                         user.values()

                    }
                },status=status.HTTP_200_OK)

        return Response ({})


        # return super().get(request, *args, **kwargs)


class addOrgDetailView(generics.RetrieveAPIView):
    serializer_class = OrgSerializer
    queryset = Organisation.objects.all()

    def get_queryset(self):
        orgId = self.kwargs['orgId']
        try:
            oid = int(orgId)
        except:
            oid = orgId
        if type(oid) ==int:
            queryset = Organisation.objects.filter(
            Q(orgId=oid) |
            Q(pk=oid))
        else:
            queryset = Organisation.objects.filter(orgId=oid)

        return queryset


    def get(self, request, *args, **kwargs):

        orgs = self.get_queryset()
        request.user.organisation.add(orgs[0])
        if orgs:
            print(orgs)
            return Response({
                "status": "success",
                "message": "<message>",
                "data": {

                         orgs.values()

                    }
                },status=status.HTTP_200_OK)