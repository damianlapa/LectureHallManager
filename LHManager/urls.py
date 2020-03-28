"""LHManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from managerapp.views import AddLectureHall, ShowAllHalls, HallsAvailability, AddReservation, EditHall, DeleteHall, \
    HallSearch

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add-lecture-hall', AddLectureHall.as_view(), name='add-lecture-hall'),
    path('halls', ShowAllHalls.as_view(), name='halls'),
    path('halls-availability', HallsAvailability.as_view(), name='halls-availability'),
    path('add-reservation', AddReservation.as_view(), name='add-reservation'),
    path('hall/modify/<hall_id>', EditHall.as_view(), name='edit-hall'),
    path('hall/delete/<hall_id>', DeleteHall.as_view(), name='delete-hall'),
    path('hall/search', HallSearch.as_view(), name='hall-search')
]
