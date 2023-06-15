"""elevator_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from elevator.views import ElevatorViewSet, RequestViewSet 
from elevator.views import submit_request, initialize_elevator_system, mark_elevator_not_operational,fetch_requests_for_elevator, get_next_destination,get_elevator_status,operate_elevator_door

router = routers.DefaultRouter()
router.register('elevators', ElevatorViewSet)
router.register('requests', RequestViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/initialize-elevator-system/', initialize_elevator_system, name='initialize_elevator_system'),
    path('api/mark-elevator-not-operational/', mark_elevator_not_operational, name='mark_elevator_not_operational'),
    path('api/fetch-requests-for-elevator/<elevator_number>/', fetch_requests_for_elevator, name='fetch_requests_for_elevator'),
    path('api/submit-request/', submit_request, name='submit-request'),
    path('api/operate_elevator_door/', operate_elevator_door, name='operate_elevator_door'),
    path('api/next-destination/<int:elevator_number>/', get_next_destination, name='get_next_destination'),
    path('api/status/<int:elevator_number>/', get_elevator_status, name='get_elevator_status'),
]
