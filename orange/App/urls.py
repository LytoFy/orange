from django.urls import path, include

urlpatterns = [
    path("home/", include(("Home.urls",'Home'), namespace='home')),
    path("user/", include(("User.urls",'User'), namespace='user')),
    path("relative/", include(("Relative.urls",'Relative'), namespace='relative')),
]