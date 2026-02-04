from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from .models import User, EmailOTP
from .serializers import UserSerializer, RegisterSerializer
import random
from django.utils import timezone
from datetime import timedelta

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_otp(request):
    email = request.data.get('email')
    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    otp_code = str(random.randint(1000, 9999))
    
    # Store in database
    EmailOTP.objects.create(email=email, otp=otp_code)
    
    print(f"OTP for {email}: {otp_code}")
    
    try:
        send_mail(
            subject='VetPathshala OTP Verification',
            message=f'Your OTP is {otp_code}. It is valid for 10 minutes.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({"message": "OTP sent successfully via email"})
    except Exception as e:
        print(f"Error sending email: {e}")
        return Response({"error": "Failed to send OTP email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_otp(request):
    email = request.data.get('email')
    otp_code = request.data.get('otp')
    
    if not email or not otp_code:
        return Response({"error": "Email and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Check database for most recent OTP in last 10 minutes
    time_threshold = timezone.now() - timedelta(minutes=10)
    otp_entry = EmailOTP.objects.filter(
        email=email, 
        otp=otp_code,
        created_at__gte=time_threshold
    ).first()

    if otp_entry:
        # Delete the OTP after use (optional but secure)
        otp_entry.delete()
        
        user = User.objects.filter(email=email).first()
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "verified": True,
                "registered": True,
                "token": token.key,
                "user": UserSerializer(user).data
            })
        return Response({"verified": True, "registered": False})
    
    return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
