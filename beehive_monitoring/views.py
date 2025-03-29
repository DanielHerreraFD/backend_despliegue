from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import status
from beehive_monitoring.serializers import MonitoringSerializerInput, MonitoringSerializerOutput
from beehive_monitoring.models import Monitoring 
from rest_framework.permissions import IsAuthenticated
from .models import Monitoring


class BeehiveMonitoringView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk=None):
        try:
            serializer = MonitoringSerializerInput(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            monitoring = Monitoring.objects.create(**serializer.validated_data)
            
            serializer_output = MonitoringSerializerOutput(monitoring)
            return Response(serializer_output.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"error": f"Error al crear el monitoreo: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class EditBeehiveMonitoringView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk=None):
        try:
            monitoring = Monitoring.objects.get(pk=pk)
        except Monitoring.DoesNotExist:
            return Response({"error": "El registro del monitoreo no existe"}, status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = MonitoringSerializerInput(monitoring, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            serializer_output = MonitoringSerializerOutput(monitoring)
            return Response(serializer_output.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"Error al actualizar el monitoreo: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class ListBeehiveMonitoringView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            
            if user.role == 'admin':
                monitorings = Monitoring.objects.all()
            else:
                monitorings = Monitoring.objects.filter(beekeeper=user)
                
            serializer = MonitoringSerializerOutput(monitorings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"Error al obtener los monitoreos: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class ListPublicBeehiveMonitoringView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            monitorings = Monitoring.objects.all().order_by('-monitoring_date')
            serializer = MonitoringSerializerOutput(monitorings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"Error al obtener los monitoreos: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)