from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import random

# In-memory store for demo purposes (Use Redis/DB in production)
otp_store = {}

@api_view(['GET'])
def health_check(request):
    return Response({"status": "healthy", "message": "Django backend is connected!"})

@api_view(['POST'])
def send_otp(request):
    """
    Simulates sending an OTP to a mobile number.
    Returns the OTP in the response for demo purposes.
    """
    phone = request.data.get('phone')
    if not phone:
        return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate 4-digit OTP
    otp = str(random.randint(1000, 9999))
    otp_store[phone] = otp
    
    print(f"-------------> OTP for {phone}: {otp} <-------------")
    
    return Response({
        "message": "OTP sent successfully",
        "otp": otp # Included for testing convenience
    })

@api_view(['POST'])
def verify_otp(request):
    """
    Verifies the OTP for a mobile number.
    """
    phone = request.data.get('phone')
    otp = request.data.get('otp')
    
    if not phone or not otp:
         return Response({"error": "Phone and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)
         
    stored_otp = otp_store.get(phone)
    if stored_otp == otp:
        # Clear OTP after successful use
        del otp_store[phone]
        return Response({"message": "Verification successful", "verified": True})
    
    return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)
