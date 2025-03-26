from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from hive_management.serializers import BeehiveSerializerInput, BeehiveSerializerOutput, EditBeehiveStatusSerializer
from hive_management.models import Beehive
import os
import qrcode
import json
import base64 
from io import BytesIO
from rest_framework.permissions import IsAuthenticated 
import environ

env = environ.Env()
environ.Env.read_env() 

class CreateHiveView(APIView):
    permission_classes = [IsAuthenticated]
    def generate_qr(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        base_url = env('BASE_URL')
        url = f"{base_url}{data}"  
        
        qr.add_data(url)  
        qr.make(fit=True)
        
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        qr_folder = "qr_images"
        os.makedirs(qr_folder, exist_ok=True)
        
        file_name = f"qr_hive_{data}.png"
        file_path = os.path.join(qr_folder, file_name)
        
        qr_image.save(file_path, format="PNG")
        
        buffered = BytesIO()
        qr_image.save(buffered, format="PNG")
        qr_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return qr_base64

    def post(self, request):
        try:
            serializer = BeehiveSerializerInput(data=request.data)
            serializer.is_valid(raise_exception=True)
            beehive = serializer.save()
            qr_code = self.generate_qr(beehive.id)  
            beehive.qr_code = qr_code
            beehive.save()
            serializer_output = BeehiveSerializerOutput(beehive)
            return Response(serializer_output.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"Error al crear la colmena: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

            


class EditHiveView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk=None):
        try:
            beehive = Beehive.objects.get(pk=pk)    
            serializer = BeehiveSerializerInput(beehive, data=request.data, partial=True)
            if serializer.is_valid():
                updated_beehive = serializer.save() 
                return Response(BeehiveSerializerOutput(updated_beehive).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Beehive.DoesNotExist:
            return Response(
                {"error": "Colmena no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )


class EditStateBeehiveView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, pk=None):
        try:
            beehive = Beehive.objects.get(pk=pk)
        except Beehive.DoesNotExist:
            return Response({"error": "La colmena no existe"}, status=status.HTTP_404_NOT_FOUND)
        
        if "status" not in request.data:
            return Response({"error": "Solo se permite modificar el estado de la colmena"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        serializer = EditBeehiveStatusSerializer(beehive, data=request.data, partial=True)
        
        if serializer.is_valid():
            beehive.status = serializer.validated_data['status']
            beehive.save()
            return Response({"message": "Estado de la colmena actualizado correctamente", 
                           "status": beehive.status}, 
                          status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetailHiveView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        try:
            beehive = Beehive.objects.get(pk=pk)
            return Response(BeehiveSerializerOutput(beehive).data)
        except Beehive.DoesNotExist:
            return Response(
                {"error": "Colmena no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )


class DetailPublicHiveView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk=None):
        try:
            beehive = Beehive.objects.get(pk=pk)
            return Response(BeehiveSerializerOutput(beehive).data)
        except Beehive.DoesNotExist:
            return Response(
                {"error": "Colmena no encontrada"},
                status=status.HTTP_404_NOT_FOUND
            )




class ListHivesView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        beehives = Beehive.objects.filter(beekeeper_id=request.user)
        return Response(BeehiveSerializerOutput(beehives, many=True).data)

class ListHiveAdmin(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        beehives = Beehive.objects.all()
        return Response(BeehiveSerializerOutput(beehives, many=True).data)