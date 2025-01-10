from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_view),
    path("<int:u_id>/", views.index, name="index"),
    # ex: /trh/5/5/
    path("<int:u_id>/<int:h_id>/", views.detail, name="detail"),
    path("<int:u_id>/<int:h_id>/setentry", views.setentry, name="setentry"),
]