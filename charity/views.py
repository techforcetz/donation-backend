from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.views import APIView
from .serializers import Charity_Serializer,Donate_Serializer,CreateCharityPhase_Serializer,ViewDonation
from rest_framework.permissions import IsAuthenticated
from .models import Charity,Donations,CharityUploads
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.

class CreateCharity(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class= Charity_Serializer
    
    def post(self,request):
        serializer = Charity_Serializer(data = request.data, context={"request":request})
        if serializer.is_valid():
            charity = serializer.save()
            return Response({"charity_id":charity.id},status=201)
        return Response(serializer.errors,status=400)

# upload the document view 
class UploadCharityDocs(APIView):
    parser_classes = [MultiPartParser, FormParser]
    # load id
    def post(self,request):
        charity_id = request.data.get("charity_id")
        charity = get_object_or_404(Charity,id = charity_id)

        document = request.FILES.get("document")
        if not document:
            return Response({"error":"no file uploaded"},status=400)
        
        upload = CharityUploads.objects.create(charity = charity,document = document)
        return Response({"message":"file upload success"},status=201)


class CreateCharityPhases(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateCharityPhase_Serializer


    def post(self,request):
        # get id from request
        charity_id = request.data.get("charity_id")
        if not charity_id:
            return Response({"error":"charity id is not provided"},status=400)
        
        # get phases
        phases_data = request.data.get("phases",[])

        for phase in phases_data:
            phase["charity_id"] = charity_id

        serializer = CreateCharityPhase_Serializer(data=phases_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"phases created successfully"},status=201)
        return Response(serializer.errors,status=400)
    

class ViewCharity(ListAPIView):
    serializer_class = Charity_Serializer
    queryset = Charity.objects.all()

class ViewUserCharity(ListAPIView):
    serializer_class = Charity_Serializer
    authentication_classes= [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Charity.objects.filter(user=self.request.user)


class DonateToCharity(CreateAPIView):
    serializer_class = Donate_Serializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class ViewUserDonation(ListAPIView):
    serializer_class = ViewDonation
    authentication_classes= [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Donations.objects.filter(user=self.request.user).select_related("charity")