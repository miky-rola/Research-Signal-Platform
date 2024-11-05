from django.urls import include, path

app_name = "api"


urlpatterns = [
    # path(r"signals/", include("apps.signals.urls")),
    path(r"", include("apps.users.urls")),
]
