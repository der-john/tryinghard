from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # ex: /trh/5/
    path("<int:h_id>/", views.detail, name="detail"),
    path("<int:h_id>/setentry", views.setentry, name="setentry"),
]