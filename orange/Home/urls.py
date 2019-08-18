from django.urls import path, include, re_path

from Home.views import *

urlpatterns = [

    path("market/", MarkIndex.as_view(), name="market"),
    path("handpeople/", NBPeople.as_view(), name="handpeople"),
    re_path(r"temphand/((\d*)?)/?", TempHand.as_view(), name="temphand"),

    re_path(r"mcenter/", MarkHand.as_view(), name="mcenter"),
    re_path(r"upload/", UploadFile.as_view(), name="upload"),

]
