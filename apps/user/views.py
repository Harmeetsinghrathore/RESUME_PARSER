from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


from .serializers import User_Serializer
from .models import User

# from lib.functions import hash_password, check_password

# Create your views here.

class RegisterView(APIView):

    def post(self, request):

        data = request.data
        serializer = User_Serializer(data = data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.active = True
            user.normal_user = True
            user.save()

            return Response({
                'message' : 'User registered successfully',
                'status' : 'success',
                'user' : serializer.data
            },
            status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

    def post(self, request):

        if request.user.is_authenticated:
            return Response({'message' : 'user already logged in.'}, status = status.HTTP_400_BAD_REQUEST)
        
        try:
            email = request.data.get('email')
        except:
            return Response({'message' : 'email field missing'}, status = status.HTTP_400_BAD_REQUEST)

        try:
            password = request.data.get('password')
        except:
            return Response({'message' : 'password field missing'}, status = status.HTTP_400_BAD_REQUEST)
        
        u = User.objects.filter(email = email).first()

        
        if u is not None:
            if u.active:
                if u.check_password(password):
                    refresh = RefreshToken.for_user(u)
                    refresh['id'] = str(u.id)
                    refresh['permissions'] = u.get_permissions()

                    return Response({
                        'message' : 'user login successfully',
                        'refresh' : str(refresh),
                        'access' : str(refresh.access_token),
                        }, status = status.HTTP_200_OK)
                else:
                    return Response({
                        'message' : 'Invalid password',
                    }, tatus = status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'message' : 'User not active'}, status = status.HTTP_401_UNAUTHORIZED)


        




                


