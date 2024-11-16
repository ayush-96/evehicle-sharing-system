from django.contrib import admin
from django.urls import path
from eVehicleSystemApp import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    #path("home/index/", views.index),
    path("home/UserLogin/", views.UserLogin),
    path("home/UserRegistration/", views.UserRegistration, name="UserRegistration"),
    path("home/UserHomePage/", views.UserHomePage),
    # path("home/UserHomePage/", views.update_selection)
    path("home/StaffLogin/", views.stafflogin),
    path("operator/operator/", views.operator_page),
    path("manager/manager_dashboard/", views.manager_dashboard),
    path("manager/User/", views.manager_userpage),
    path("manager/Location/", views.manager_locationpage),
    path("manager/Vehicles/", views.manager_vehiclepage),
    path("home/AboutUs/", views.about_us),
    path("home/Settings/", views.Settings),
    path("home/Privacy/", views.Privacy),
    path("home/Notifications/", views.Notifications)
    
]