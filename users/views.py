from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import InputUserSerializer, OutputUserSerializer
from users.serializers import LoginInputSerializer, LoginOutputSerializer
from users.serializers import PasswordResetRequestSerializer, PasswordResetSerializer
from users.models import CustomUser, Login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import environ

env = environ.Env()
environ.Env.read_env()

class canCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            users = CustomUser.objects.all()

            if not users.exists():
                return Response({"message": "Register"}, status=status.HTTP_200_OK)

            return Response({"message": "Login"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": f"Error inesperado: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class singUpView(APIView):
    permission_classes = [AllowAny]

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
        
class loginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            user = CustomUser.objects.get(username=serializer.validated_data['username'])
        except CustomUser.DoesNotExist:
            return Response({'Error':'Usuario o Contraseña es incorrecta'}, status=status.HTTP_400_BAD_REQUEST)
        
        is_password_correct = user.check_password(serializer.validated_data['password'])
        if is_password_correct is False:
            return Response({'Error': 'Usuario o Contraseña es incorrecta'}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.state != 'Active':
            return Response({'Error': 'Tu cuenta está desactivada.'}, status=status.HTTP_403_FORBIDDEN)


        refresh = RefreshToken.for_user(user)

        Login.objects.create(username=user.username, password="hashed", date_login=timezone.now(), id_User=user) 

        serializer = LoginOutputSerializer({
            "username": user.username,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "role": user.role,
            "id_User": user.id,
            "state" : user.state
        })
        return Response(data=serializer.data, status=status.HTTP_200_OK)
class PasswordResetRequestView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        print("\n[DEBUG] Iniciando proceso de reset de contraseña")
        print(f"[DEBUG] Datos recibidos: {request.data}")
        
        # Validar datos de entrada
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print(f"[ERROR] Datos inválidos: {serializer.errors}")
            return Response(
                {'error': 'Datos inválidos', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data['email']
        print(f"[DEBUG] Email validado: {email}")
        
        env = environ.Env()
        print("[DEBUG] Variables de entorno cargadas")
        
        try:
            # 1. Buscar usuario
            try:
                print("[DEBUG] Buscando usuario en la base de datos...")
                user = CustomUser.objects.get(email=email)
                print(f"[DEBUG] Usuario encontrado: ID {user.id}, {user.email}")
            except CustomUser.DoesNotExist:
                print(f"[WARNING] No existe usuario con email: {email}")
                return Response(
                    {'message': 'Si este correo existe en nuestro sistema, recibirás un enlace para restablecer tu contraseña.'},
                    status=status.HTTP_200_OK
                )

            # 2. Generar token y URL
            try:
                print("[DEBUG] Generando token y URL de reset...")
                token = default_token_generator.make_token(user)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                print(f"[DEBUG] Token generado: {token}")
                print(f"[DEBUG] UIDB64 generado: {uidb64}")
                
                frontend_url = env('FRONTEND_URL')
                print(f"[DEBUG] FRONTEND_URL: {frontend_url}")
                
                reset_url = f"{frontend_url}/ConfirmPassword/{uidb64}/{token}"
                print(f"[DEBUG] URL completa: {reset_url}")
            except Exception as e:
                print(f"[ERROR] Fallo generando token/URL: {str(e)}")
                return Response(
                    {'error': 'Error al generar el enlace de recuperación.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # 3. Enviar email
            try:
                print("[DEBUG] Preparando email...")
                context = {
                    'user': user.username,
                    'reset_url': reset_url
                }
                print(f"[DEBUG] Contexto email: {context}")
                
                html_message = render_to_string('emails/password_reset.html', context)
                plain_message = strip_tags(html_message)
                print("[DEBUG] Plantilla de email renderizada")
                
                email_from = env('EMAIL_HOST_USER')
                print(f"[DEBUG] Email FROM: {email_from}")
                print(f"[DEBUG] Email TO: {email}")
                
                print("[DEBUG] Enviando email...")
                send_mail(
                    'Restablecimiento de contraseña',
                    plain_message, 
                    email_from,
                    [email],
                    fail_silently=False,
                    html_message=html_message
                )
                print("[DEBUG] Email enviado exitosamente!")
                
                return Response(
                    {'message': 'Si este correo existe en nuestro sistema, recibirás un enlace para restablecer tu contraseña.'},
                    status=status.HTTP_200_OK
                )

            except Exception as e:
                print(f"[ERROR CRÍTICO] Fallo enviando email: {str(e)}")
                return Response(
                    {'error': 'Error al enviar el correo electrónico de recuperación.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except Exception as e:
            print(f"[ERROR GLOBAL] Error inesperado: {str(e)}")
            return Response(
                {'error': 'Ocurrió un error inesperado. Por favor, inténtalo de nuevo más tarde.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )    
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):  
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            password2 = serializer.validated_data['password2']

            if password != password2:
                return Response({'error': 'Las contraseñas no coinciden.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = CustomUser.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
                return Response({'error': 'Token inválido.'}, status=status.HTTP_400_BAD_REQUEST)

            if not default_token_generator.check_token(user, token):
                return Response({'error': 'Token inválido.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(password)
            user.save()

            return Response({'message': 'Contraseña restablecida con éxito.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    
