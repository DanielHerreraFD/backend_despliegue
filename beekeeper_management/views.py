from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from beekeeper_management.serializers import InputUserSerializer, OutputUserSerializer, InpuEditUserSerializer, OutPutUserDetailSerializer, EditUserStateSerializer
from users.models import CustomUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminRole
from rest_framework_simplejwt.authentication import JWTAuthentication

class createBeekeeperView(APIView):
    authentication_classes = [JWTAuthentication]  
    permission_classes = [IsAuthenticated, IsAdminRole]  

    def post(self, request):
        try:
            serializer = InputUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            
            if CustomUser.objects.filter(username=serializer.validated_data["username"]).exists():
                return Response({'error': 'El usuario ya está registrado'}, status=status.HTTP_400_BAD_REQUEST)

            if CustomUser.objects.filter(email=serializer.validated_data["email"]).exists():
                return Response({'error': 'El email ya está registrado'}, status=status.HTTP_400_BAD_REQUEST)

            
            user = CustomUser.objects.create(
                username=serializer.validated_data["username"],
                first_name=serializer.validated_data["first_name"],
                last_name=serializer.validated_data["last_name"],
                identifications=serializer.validated_data["identifications"],
                email=serializer.validated_data["email"],
                phone=serializer.validated_data["phone"],
                assignment_date=serializer.validated_data["assignment_date"],
                birth_date=serializer.validated_data["birth_date"],
                state=serializer.validated_data["state"],
                emergency_contact_name=serializer.validated_data["emergency_contact_name"],
                emergency_contact_phone=serializer.validated_data["emergency_contact_phone"],
                role=serializer.validated_data["role"],
            )

            
            user.set_password(serializer.validated_data["password"])
            user.save()

            
            refresh = RefreshToken.for_user(user)

            
            serializer_output = OutputUserSerializer({
                "id": user.id,
                "username": user.username,
                "identifications": user.identifications,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone": user.phone,
                "assignment_date": user.assignment_date,
                "birth_date": user.birth_date,
                "state": user.state,
                "emergency_contact_name": user.emergency_contact_name,
                "emergency_contact_phone": user.emergency_contact_phone,
                "role": user.role,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            })

            return Response(data=serializer_output.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Error inesperado: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    

class editBeekeeperView(APIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated, IsAdminRole]  

    def patch(self, request, pk=None):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"error": "El usuario no existe"}, status=status.HTTP_404_NOT_FOUND)

        serializer = InpuEditUserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            for key, value in serializer.validated_data.items():
                setattr(user, key, value)
            user.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class editStateBeekeeperView(APIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated, IsAdminRole]  

    def patch(self, request, pk=None):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"error": "El usuario no existe"}, status=status.HTTP_404_NOT_FOUND)

    
        if "state" not in request.data:
            return Response({"error": "Solo se permite modificar el estado"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EditUserStateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            user.state = serializer.validated_data['state']
            user.save()
            return Response({"message": "Estado actualizado correctamente", "state": user.state}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        

class detailBeekeeperView(APIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated]  
    
    def get(self, request, pk=None):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({"error": "el usuario no exite"}, status=status.HTTP_404_NOT_FOUND)
        serializer = OutPutUserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)



class listBeekeepersView(APIView):
    authentication_classes = [JWTAuthentication] 
    permission_classes = [IsAuthenticated, IsAdminRole]  
    

    def get(self, request):
        try:
            users = CustomUser.objects.all()

            if not users.exists():
                return Response({"message": "No hay apicultores registrados."}, status=status.HTTP_204_NO_CONTENT)

            serializer = OutPutUserDetailSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


        except Exception as e:
            return Response({"error": f"Error inesperado: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)