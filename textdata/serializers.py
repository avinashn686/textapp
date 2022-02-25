
import logging
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from textdata.models import TextTable, TextTitle
logger = logging.getLogger(__name__)
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user




class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']






class CreateTextSeriallizer(ModelSerializer):

    class Meta:
            model = TextTable
            fields = [
                "id",
                "text",
                "title",
                "item_text"
            ]

    def create(self, validated_data):
        requests = self._kwargs["context"].get("request")
        texttitle = (
            validated_data.pop("item_text")
            if "item_text" in validated_data
            else None)

        project_obj = TextTable.objects.create(**validated_data)
        if texttitle:
            for texttitles in texttitle:
                project_obj.item_text.add(texttitles)
        
        return project_obj

    def update(self,instance, validated_data):
        texttitle = (
            validated_data.pop("item_text")
            if "item_text" in validated_data
            else None)
        fields = instance._meta.fields
        for field_name in fields:
            setattr(
                instance,
                field_name.name,
                validated_data.get(field_name.name, getattr(instance, field_name.name)),
            )

        instance.save()
        if texttitle:
            instance.item_text.set(texttitle)      
        return instance

class CreateTexttitleSeriallizer(ModelSerializer):

    class Meta:
            model = TextTitle
            fields = [
                "id",
                "title",
            ]


class TextTableListSerializer(ModelSerializer):
    created_by = SerializerMethodField(read_only=True)
    item_text = SerializerMethodField(read_only=True)
    def get_created_by(self, obj):
        try:
            if obj.created_by:
                created_by_dict = {
                    "id": obj.created_by.id,
                    "value": obj.created_by.first_name,
                }
                return created_by_dict
            else:
                return None
        except Exception as exception:
            logger.exception(
                "Getting Exception while Fetching Created by as %s", exception
            )
            return None
    def get_item_text(self, obj):

        try:
            if obj.item_text:
                text_item = list()
                data = obj.item_text.all()
                for items in data:
                    text_item.append({"id": items.id, "title": items.title})
                return text_item
        except Exception as exception:
            logger.exception("Getting Exception while Fetching title as %s", exception)
            return None
    class Meta:
        model = TextTable
        fields = ['id','object_id','text','title','modified_at','created_by','item_text']

class TitleTableListSerializer(ModelSerializer):
    
    class Meta:
        model = TextTitle
        fields = '__all__'
class TextTaggingSerializer(ModelSerializer):
    class Meta:
        model = TextTitle
        exclude=['title']