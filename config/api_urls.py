from django.urls import include, path

app_name = "api"


urlpatterns = [
    path(r"", include("apps.users.urls")),
]
