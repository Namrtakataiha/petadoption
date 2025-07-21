from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import User, Pet, Category, AdoptionApplication
from .serializers import UserSerializer, PetSerializer, CategorySerializer, AdoptionApplicationSerializer
from .permissions import IsAdminUserOrReadOnly
from .models import AdoptionApplication
import random
# from django.contrib.auth import authenticate
from .models import User, UserOTP
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail

@api_view(['POST'])
def register_user(request):
    data = request.data
    required_fields = ['username', 'email', 'password', 'mobile_no', 'address']
    for field in required_fields:
        if not data.get(field):
            return Response({field: "This field is required."}, status=400)

    email = data.get('email')
    try:
        user = User.objects.get(email=email)
        if user.is_verified:
            return Response({"message": "User already registered and verified."}, status=400)
        else:
            # If user exists but not verified, resend OTP
            otp = str(random.randint(100000, 999999))
            UserOTP.objects.create(user=user, otp=otp)

            send_mail(
                'Your User OTP Verification Code',
                f'Your OTP is {otp}',
                'kataihanamrta380@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "User already registered but not verified. OTP resent to your email."}, status=200)
    except User.DoesNotExist:
        pass  # Proceed to create new user

    # Create new user
    data['password'] = make_password(data['password'])
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save(is_admin=False, is_verified=False)

        otp = str(random.randint(100000, 999999))
        UserOTP.objects.create(user=user, otp=otp)

        send_mail(
            'Your User OTP Verification Code',
            f'Your OTP is {otp}',
            'kataihanamrta380@gmail.com',
            [user.email],
            fail_silently=False,
        )

        return Response({"message": "User registered. OTP sent to your email for verification."}, status=201)
    return Response(serializer.errors, status=400)



# ✅ Verify User OTP
@api_view(['POST'])
def veri_user(request):
    email = request.data.get('email')
    otp = request.data.get('otp')

    if not email or not otp:
        return Response({"message": "Email and OTP are required"}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    try:
        user_otp = UserOTP.objects.filter(user=user).latest('created_at')
    except UserOTP.DoesNotExist:
        return Response({"message": "OTP not found"}, status=404)

    if user_otp.otp != otp:
        return Response({"message": "Invalid OTP"}, status=400)

    user.is_verified = True
    user.save()
    user_otp.delete()

    return Response({"message": "User verified successfully"}, status=200)


# ✅ Register Admin
@api_view(['POST'])
def register_admin(request):
    data = request.data
    required_fields = ['username', 'email', 'password', 'mobile_no', 'address']
    for field in required_fields:
        if not data.get(field):
            return Response({field: "This field is required."}, status=400)

    data['password'] = make_password(data['password'])
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save(is_admin=True, is_staff=True, is_verified=False)

        otp = str(random.randint(100000, 999999))
        UserOTP.objects.create(user=user, otp=otp)

        send_mail(
            'Your Admin OTP Verification Code',
            f'Your OTP is {otp}',
            'noreply@yourdomain.com',
            [user.email],
            fail_silently=False,
        )

        return Response({"message": "Admin registered. OTP sent to email for verification."}, status=201)
    return Response(serializer.errors, status=400)


# ✅ Verify Admin OTP
@api_view(['POST'])
def veri_admin(request):
    email = request.data.get('email')
    otp = request.data.get('otp')

    if not email or not otp:
        return Response({"message": "Email and OTP are required"}, status=400)

    try:
        user = User.objects.get(email=email, is_admin=True)
    except User.DoesNotExist:
        return Response({"message": "Admin not found"}, status=404)

    try:
        user_otp = UserOTP.objects.filter(user=user).latest('created_at')
    except UserOTP.DoesNotExist:
        return Response({"message": "OTP not found"}, status=404)

    if user_otp.otp != otp:
        return Response({"message": "Invalid OTP"}, status=400)

    user.is_verified = True
    user.save()
    user_otp.delete()

    return Response({"message": "Admin verified successfully"}, status=200)


# ✅ Login User
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"message": "Username and password are required"}, status=400)

    try:
        user = User.objects.get(username=username, is_admin=False)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    if not user.is_verified:
        return Response({"message": "User is not verified"}, status=403)

    if not check_password(password, user.password):
        return Response({"message": "Incorrect password"}, status=400)

    refresh = RefreshToken.for_user(user)
    return Response({
        'message': 'User login successful',
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    })


# ✅ Login Admin
@api_view(['POST'])
def login_admin(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"message": "Username and password are required"}, status=400)

    try:
        user = User.objects.get(username=username, is_admin=True)
    except User.DoesNotExist:
        return Response({"message": "Admin not found"}, status=404)

    if not user.is_verified:
        return Response({"message": "Admin is not verified"}, status=403)

    if not check_password(password, user.password):
        return Response({"message": "Incorrect password"}, status=400)

    refresh = RefreshToken.for_user(user)
    return Response({
        'message': 'Admin login successful',
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    })

# 





# @api_view(['POST'])
# def login(request):
#     username_or_mobile = request.data.get('username')
#     password = request.data.get('password')

#     if not username_or_mobile or not password:
#         return Response({"message": "Username/mobile and password are required"}, status=400)

#     try:
#         user = User.objects.get(username=username_or_mobile)
#     except User.DoesNotExist:
#         return Response({"message": "User not found. Please register first."}, status=404)

#     user_auth = authenticate(username=user.username, password=password)

#     if user_auth is not None:
#         # ✅ Generate JWT tokens
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)
#         refresh_token = str(refresh)

#         return Response({
#             "message": "Login successful",
#             "access_token": access_token,
#             "refresh_token": refresh_token,
#             "token_validity": "5 days"
#         }, status=200)

#     else:
      
#         return Response({
#             "message": "Incorrect password. Please reset your password using forgot password option."
#         }, status=401)




@api_view(['POST'])
def reset_password(request):
    mobile = request.data.get('mobile')
    otp = request.data.get('otp')
    new_password = request.data.get('new_password')

    if not mobile:
        return Response({"message": "Mobile is required"}, status=400)

    try:
        user = User.objects.get(username=mobile)  # Adjust if your model uses mobile_no field instead
    except User.DoesNotExist:
        return Response({"message": "User with this mobile not found. Please register first."}, status=404)

    # ✅ If OTP and new_password not provided ➔ generate OTP and send via email
    if not otp or not new_password:
        generated_otp = str(random.randint(100000, 999999))
        UserOTP.objects.create(user=user, otp=generated_otp)

        # ✅ Send OTP to user's email
        send_mail(
            subject='Your Password Reset OTP',
            message=f'Your OTP code for password reset is {generated_otp}',
            from_email='noreply@yourdomain.com',
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response({
            "message": "OTP generated and sent to your registered email. Please provide OTP and new password to reset."
        })

    # ✅ If OTP and new_password provided ➔ verify OTP
    try:
        user_otp = UserOTP.objects.filter(user=user).latest('created_at')
    except UserOTP.DoesNotExist:
        return Response({"message": "No OTP found. Please request again."}, status=404)

    if user_otp.otp != otp:
        return Response({"message": "Invalid OTP. Please try again."}, status=400)

    # ✅ Set new password
    user.set_password(new_password)
    user.save()

    return Response({"message": "Password reset successful. You can now login with your new password."}, status=200)

# ✅ 2. Reset password API - verifies OTP and resets password
# @api_view(['POST'])
# def reset_password(request):
#     mobile = request.data.get('mobile')
#     otp = request.data.get('otp')
#     new_password = request.data.get('new_password')

#     if not mobile:
#         return Response({"message": "Mobile is required"}, status=400)

#     try:
#         user = User.objects.get(username=mobile)
#     except User.DoesNotExist:
#         return Response({"message": "User with this mobile not found. Please register first."}, status=404)

#     # ✅ If OTP and new_password not provided ➔ generate OTP and ask for them
#     if not otp or not new_password:
#         generated_otp = str(random.randint(100000, 999999))
#         UserOTP.objects.create(user=user, otp=generated_otp)
#         print(f"OTP for password reset: {generated_otp}")

#         return Response({
#             "message": "OTP generated and sent to your registered mobile. Please provide OTP and new password to reset."
#         })

#     # ✅ If OTP and new_password provided ➔ verify OTP
#     try:
#         user_otp = UserOTP.objects.filter(user=user).latest('created_at')
#     except UserOTP.DoesNotExist:
#         return Response({"message": "No OTP found. Please request again."}, status=404)

#     if user_otp.otp != otp:
#         return Response({"message": "Invalid OTP. Please try again."}, status=400)

#     # ✅ Set new password
#     user.set_password(new_password)
#     user.save()

#     return Response({"message": "Password reset successful. You can now login with your new password."}, status=200)




# ✅ Pet List and Create API
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def pet_list_create(request):
    if request.method == 'GET':
        pets = Pet.objects.all()
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Pet Detail API (Retrieve, Update, Delete)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def pet_detail(request, pk):
    try:
        pet = Pet.objects.get(pk=pk)
    except Pet.DoesNotExist:
        return Response({"error": "Pet not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PetSerializer(pet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PetSerializer(pet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        pet.delete()
        return Response({"message": "Pet deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    
    
@api_view(['GET', 'POST'])
@permission_classes([IsAdminUserOrReadOnly])
def category_list_create(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Apply for adoption (user only)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def apply_for_adoption(request):
    data = request.data.copy()
    data['user'] = request.user.id  
    serializer = AdoptionApplicationSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
@permission_classes([permissions.IsAdminUser]) 
def update_adoption_status(request, pk):
    try:
        application = AdoptionApplication.objects.get(pk=pk)
    except AdoptionApplication.DoesNotExist:
        return Response({"message": "Application not found"}, status=404)
    
    status = request.data.get('status')
    if status not in ['Pending', 'Approved', 'Rejected']:
        return Response({"message": "Invalid status value"}, status=400)

    application.status = status
    application.save()
    return Response({"message": "Status updated successfully", "new_status": application.status})




# View user adoption applications and their status
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_adoptions(request):
    
    
    apps = AdoptionApplication.objects.filter(user=request.user)
    serializer = AdoptionApplicationSerializer(apps, many=True)
    return Response(serializer.data)

# Admin view all adoptions (dashboard)
@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def all_adoptions(request):
    apps = AdoptionApplication.objects.all()
    serializer = AdoptionApplicationSerializer(apps, many=True)
    return Response(serializer.data)
