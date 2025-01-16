from django.http import JsonResponse
import logging
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Role
from .serializers import UserSerializer, RoleSerializer, LoginSerializer
from .services import get_etherscan_transactions, get_crypto_prices


logger = logging.getLogger('django')

def test_logging(request):
    logger.debug("Test log message")
    return JsonResponse({"message": "Logged"})


@api_view(['GET'])
def transactions(request):
    address = request.query_params.get('address')
    if not address:
        return Response({"error": "Address is required"}, status=400)
    data = get_etherscan_transactions(address)
    return Response(data)

@api_view(['GET'])
def prices(request):
    symbol = request.query_params.get('symbol')
    if not symbol:
        return Response({"error": "Symbol is required"}, status=400)
    data = get_crypto_prices(symbol)
    return Response(data)


class RoleView(APIView):
    def post(self, request):
        data = request.data
        name = data.get("name")
        try:
            if not name:
                return Response({"error": "Name is equired."}, status=status.HTTP_400_BAD_REQUEST)
            role = Role.objects.create(
                name=name,
            )
            serializer = RoleSerializer(role)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RegisterView(APIView):
   def post(self, request):
        data = request.data
        password = data.get("password")
        username = data.get("username")
        email = data.get("email")
        
        try:
            if not password or not username or not email:
                return Response({"error": "Email, password and username are required."}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(password) < 8:
                return Response({"error": "Password must be at least 8 characters long."}, status=status.HTTP_400_BAD_REQUEST)
            if not any(char.isdigit() for char in password):
                return Response({"error": "Password must contain at least one digit."}, status=status.HTTP_400_BAD_REQUEST)
            if not any(char.isupper() for char in password):
                return Response({"error": "Password must contain at least one uppercase letter."}, status=status.HTTP_400_BAD_REQUEST)

            role_id = data.get("role")
            if role_id:
                role = Role.objects.get(id=role_id)
            else:
                role = None
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password, 
                role=role
            )
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Role.DoesNotExist:
            return Response({"error": "Role not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class LoginView(APIView):
    def post(self, request):
        # serializer = LoginSerializer(data=request.data)
        data=request.data
        print(data)
        # if serializer.is_valid():
            # print(serializer.data) 
            # username = serializer.validated_data['username']
            # password = serializer.validated_data['password']
        if data:
            credentials = {
            "username" : data.get("username"),
            "password" : data.get("password")
            }
            print(f"{credentials}")

            user = authenticate(request, username=data.get("username"), password=data.get("password"))

            if user is None:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            
            # login(request, user)
            print(f"User {user.username} logged in.")
            refresh = RefreshToken.for_user(user)

            return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "RData not found"}, status=status.HTTP_400_BAD_REQUEST)