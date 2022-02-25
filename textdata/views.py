import logging
from django.shortcuts import render
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from textdata.models import TextTable, TextTitle
from textdata.serializers import UserSerializer, GroupSerializer
# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions,status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import logout
from textdata.serializers import UserSerializer, GroupSerializer
from rest_framework.decorators import  permission_classes,api_view
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CreateTextSeriallizer, CreateTexttitleSeriallizer, MyTokenObtainPairSerializer, TextTableListSerializer, TextTaggingSerializer, TitleTableListSerializer
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.exceptions import APIException,NotFound
from rest_framework import generics
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     RetrieveUpdateAPIView)

logger = logging.getLogger(__name__)
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class CreateTextView(CreateAPIView):

    serializer_class = CreateTextSeriallizer

    """Create a new record"""

    def perform_create(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                text_ob=serializer.save(created_by=self.request.user)
                data['status'] = 'success'
                data['message'] = ' Created Successfully'
                
            else:
                data['message'] = 'creation failed due to the following errors.'
                data['details'] = serializer.errors
                data['status'] = 'failed'
                                                
        except Exception as e:
            logger.exception(f"Exception occuring while fetching Request{e}")
            raise APIException(f'something_went_wrong:{e}')

        return data

        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = self.perform_create(serializer)
        if data['status'] == 'success':
            return Response(data=data, status=200)
        else:
            return Response(data=data, status=500)


class CreateTexttitleView(CreateAPIView):

    serializer_class = CreateTexttitleSeriallizer

    """Create a new record"""

    def perform_create(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                title=serializer.data.get('title')
                text_ob=TextTitle.objects.create(title=title)
                data['status'] = 'success'
                data['message'] = ' Created Successfully'
                
            else:
                data['message'] = 'creation failed due to the following errors.'
                data['details'] = serializer.errors
                data['status'] = 'failed'
                                                
        except Exception as e:
            logger.exception(f"Exception occuring while fetching Request{e}")
            raise APIException(f"something_went_wrong:{e}")

        return data

        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = self.perform_create(serializer)
        if data['status'] == 'success':
            return Response(data=data, status=200)
        else:
            return Response(data=data, status=500)

class EditTextView(RetrieveUpdateAPIView):
    queryset = TextTable.objects.order_by('id').all()
    serializer_class = CreateTextSeriallizer
    lookup_field = "object_id"

    def perform_update(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                compliance_obj = serializer.save()
                    
                data["message"] = "text_edited_successfully"
                data["status"] = "success"
                data["code"] = 200
            
            else:
                data["message"] = "update_failed"
                data["details"] = serializer.errors
                data["status"] = "failed"
                data['code'] = 422
        except Exception as exception:
            logger.exception("Something went wrong %s", exception)
            data["status"] = "failed"
            data["message"] = 'something_went_wrong'
            data['code'] = 500
        return data
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        data = self.perform_update(serializer)
        http_code = data.pop('code',None)
        return Response(data=data, status=http_code)


class TextListView(ListAPIView):
    """
    List of all Compliance Audit
    """
    serializer_class = TextTableListSerializer
    # overriding the method

    def get_queryset(self, *args, **kwargs):
        queryset_list = list()

        queryset_list = TextTable.objects.all().order_by("-id")
       
        return queryset_list

class TextListDetailView(ListAPIView):
    """
    List of all Compliance Audit
    """
    serializer_class = TextTableListSerializer
    # overriding the method

    def get_queryset(self, *args, **kwargs):
        queryset_list = list()
        object_id=self.kwargs.get("object_id")
        queryset_list = TextTable.objects.filter(object_id=object_id)
       
        return queryset_list


class TextDeleteView(DestroyAPIView):
    """
    BusinessProcess Delete API View
    """

    queryset = TextTable.objects.all().order_by("id")
    serializer_class = TextTableListSerializer
    lookup_field = "object_id"

    def perform_destroy(self, instance):
        data = {}
        try:
            self.object_id = self.kwargs.get("object_id")
            process_obj = TextTable.objects.get(object_id=self.object_id)
            process_obj.delete()
            data["status"] = 'success'
            data["message"] = "deleted"
            data["code"] = 200
        
        except Exception as exception:
            logger.exception("Exception occuring while fetching Request %s", exception)
            data['message'] = 'something_went_wrong'
            data['status'] = 'failed'
            data['code'] = 500
        return data
                        

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.perform_destroy(instance)
        http_code = data.pop('code',None)
        return Response(data=data, status=http_code)


class Tagtitleview(RetrieveUpdateAPIView):
    queryset = TextTable.objects.only("object_id", "id")
    serializer_class = TextTaggingSerializer
    lookup_field = "object_id"

    def perform_update(self, serializer, request, *args, **kwargs):
        object_id = self.kwargs.get("object_id")
        tags = self.request.data["tags"]
        try:
            data = {}
            if serializer.is_valid():
                text_obj = TextTable.objects.get(object_id=object_id)
                text_title = TextTitle.objects.filter(object_id__in=tags)
                for obj in text_title:
                    try:
                        text_obj.item_text.add(obj)
                        
                    except Exception as exception:
                        logger.exception(exception)
                        return {
                            "status": "error",
                            "message": "something_went_wrong",
                            "code": 500,
                        }
                return {
                    "status": "success",
                    "message": "added",
                    "code": 200,
                }
            else:
                data["message"] = "update_failed"
                data["details"] = serializer.errors
                data["status"] = "failed"
                data["code"] = 422

        except Exception as exception:
            logger.exception(exception)
            return {
                "status": "error",
                "message":"something_went_wrong",
                "code": 500,
            }
        return data

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        data = self.perform_update(serializer, request)
        http_code = data.pop("code", None)
        return Response(data=data, status=http_code)

class Titledetailview(ListAPIView):
    """
    List of all Compliance Audit
    """
    serializer_class = TitleTableListSerializer
    # overriding the method

    def get_queryset(self, *args, **kwargs):
        queryset_list = list()

        queryset_list = TextTitle.objects.all().order_by("-id")
       
        return queryset_list