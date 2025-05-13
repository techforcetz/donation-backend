from django.urls import path
from .views import CreateCharity,ViewCharity,DonateToCharity,UploadCharityDocs,CreateCharityPhases,ViewUserCharity,ViewUserDonation

urlpatterns = [
    path("create_charity",CreateCharity.as_view(),name="create_charity"),
    path("view_charity",ViewCharity.as_view(),name="view_charity"),
    path("my_charity",ViewUserCharity.as_view(),name="my_charity"),
    path("my_donation",ViewUserDonation.as_view(),name="my_donation"),


    path("donate",DonateToCharity.as_view(),name="donate"),
    path("upload_doc",UploadCharityDocs.as_view(),name="upload_doc"),
    path("charity_phases",CreateCharityPhases.as_view(),name="charity_phases")

]
