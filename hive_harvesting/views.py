from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import InputHarvestingSerializer, OutputHarvestingSerializer
from .models import harvesting

class HiveHarvestingView(APIView):
    def post(self, request, pk=None):
        try:
            serializer = InputHarvestingSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            if not serializer.is_valid():
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            harvesting_v= harvesting.objects.create(**serializer.validated_data)
            
            serializer_output = OutputHarvestingSerializer(harvesting_v)
            return Response(serializer_output.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Error al crear la recoleccion: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class EditHiveHarvestingView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, pk=None):
        try:
            harvest = harvesting.objects.get(pk=pk)
        except harvesting.DoesNotExist:
            return Response({"error": "El registro de la colmena no existe"}, status=status.HTTP_404_NOT_FOUND)
        serializer = InputHarvestingSerializer(harvest, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            serializer = OutputHarvestingSerializer(harvest)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListHiveHarvestingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            
            if user.role == 'admin':
                harvests = harvesting.objects.all()
            else:
                harvests = harvesting.objects.filter(beekeeper=user)
                
            serializer = OutputHarvestingSerializer(harvests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"Error al obtener las cosechas: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
class ListPublicHiveHarvestingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            harvests = harvesting.objects.filter(beekeeper=user).order_by('-harvest_date')
            serializer = OutputHarvestingSerializer(harvests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"Error al obtener las cosechas: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)