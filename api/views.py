from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.hashers import make_password
from .models import User, Pet, Category, AdoptionApplication
from .serializers import UserSerializer, PetSerializer, CategorySerializer, AdoptionApplicationSerializer
from .permissions import IsAdminUserOrReadOnly
from .models import AdoptionApplication

# User registration (normal user)
@api_view(['POST'])
def register_user(request):
    data = request.data
    data['password'] = make_password(data['password'])
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save(is_admin=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Admin registration
@api_view(['POST'])
def register_admin(request):
    data = request.data
    data['password'] = make_password(data['password'])
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save(is_admin=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
