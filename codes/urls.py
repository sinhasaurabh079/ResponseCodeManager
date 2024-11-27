from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup_user, name="signup"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("search/", views.search_codes, name="search"),
    path("saved-lists/", views.view_saved_lists, name="saved_lists"),
    path(
        "saved-lists/<int:list_id>/", views.saved_list_detail, name="saved_list_detail"
    ),
    path("edit/<int:list_id>/", views.edit_list, name="edit_list"),
    path("delete/<int:list_id>/", views.delete_list, name="delete_list"),
]
