from django.shortcuts import render
from rest_framework import generics
from .serializer import Userserializers, UserRegistrationSerializer, LoginSerializer, UserForgetPasswordForemailSerializer, UserResetPasswordSerializer, UserUpdateSerializer
from .models import UserModel, NEW, UserCodeModel, VERIFIED
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.utils import timezone
from shared.utils import send_to_email_code
from shared.permisions import IsOwner

class UserRegiterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    model = UserModel
    serializer_class = UserRegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "status": True,
                "message": "Successfully registered, code sent to your email",
                "access_token": serializer.data['access_token'],
                "auth_status": serializer.data['auth_status']
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyRegistartions(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = self.request.user
        code = request.data['code']
        
        verify_code = UserCodeModel.objects.filter(user=user, code=code, is_confirmed=False, expiration_time__gte=timezone.now())
        
        if not verify_code.exists():
            return Response({"status": False, "message": "Wrong code"})
       
        UserCodeModel.objects.update(is_confirmed=True)
       
        user.auth_status = VERIFIED
        user.save()
            
            
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        response = {
			    "status": True,
			    "access_token": access_token,
			    "auth_status": VERIFIED
		    }
            
        return Response(response) 
        
        
class LoginUserView(APIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            
            return Response(validated_data, status=status.HTTP_200_OK)
        


class ResendVerifyCode(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = self.request.user

        verification_code = UserCodeModel.objects.filter(
            user_id=user.id, is_confirmed=False, expiration_time__gte=timezone.now())
        
        if verification_code.exists():
            response = {
                'success': False,
                'message': "You have active verification code",
            }
            return Response(response, status=status.HTTP_200_OK)
       
        self.send_code_again()
        response = {
			"status": True,
			"message": "Code send successfully",
			"auth_status": NEW
		}
        return Response(response, status=status.HTTP_200_OK)
    
    def send_code_again(self):
        user = self.request.user
        new_code = user.create_verify_code()
        send_to_email_code(user.email, new_code)
        
    
    
class UserForgetPasswordToEmail(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserForgetPasswordForemailSerializer
    
    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = UserModel.objects.get(email=email, auth_status='VERIFIED')
                
            except UserModel.DoesNotExist:
                return Response({
                    "status": False,
                    "message": "User not found or not verified"
                }, status=status.HTTP_404_NOT_FOUND)
            
            try:
                code = user.create_verify_code()  
                send_to_email_code(user.email, code)
                return Response({
                    "status": True,
                    "message": "Code sent to email"
                }, status=status.HTTP_200_OK)
                
            except Exception as e:
                return Response({
                    "status": False,
                    "message": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserResetPasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['put', 'patch']
    serializer_class = UserResetPasswordSerializer
    
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        response = super(UserResetPasswordView, self).update(request, *args, **kwargs)
        
        try:
            user = UserModel.objects.get(id=response.data.get('id'))
            
        except:
            raise Response({'success': False, 'message': 'User not found'}, status='User not found')
        
        response = {
			"status": True,
			"message": "Password changed"
		}
        
        return Response(response, status=status.HTTP_200_OK)
    
    
class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]  

    def get_object(self):
        return self.request.user
    
    
class UserdetailView(generics.RetrieveAPIView):
    serializer_class = Userserializers
    permission_classes = [IsAuthenticated]
    queryset = UserModel.objects.all()
    def get_object(self):
        return self.request.user

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)