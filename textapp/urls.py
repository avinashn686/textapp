"""textapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers
from textdata import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from textdata import views
from textdata.views import *

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('create/text/', CreateTextView.as_view(), name='create_text'),
    path('create/text/title', CreateTexttitleView.as_view(), name='create_title_text'),
    path('edit/text/<str:object_id>/', EditTextView.as_view(), name='edit_text'),
    path("text/list/",views.TextListView.as_view()),
    path("text/list-detail/<str:object_id>/",views.TextListDetailView.as_view()),
    path("title/list/",views.Titledetailview.as_view()),
    path(
        "text-delete/<str:object_id>/",views.TextDeleteView.as_view(),
        name="text-delete-api",
    ),
    path(
        "text-taging/<str:object_id>/",views.Tagtitleview.as_view(),
        name="text-tag-api",
    ),
]