from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth
from .models import Child
from account.models import Role
from .image import upload

@api_view(['GET', 'POST', 'PATCH'])
def child(request, pk=None):
    try:
        # Extracting the Firebase ID token from the Authorization header
        id_token = request.headers.get('Authorization').split(" ")[1]
        decoded_token = auth.verify_id_token(id_token)
    except Exception as e:
        return Response({'msg': 'Unauthorized: Invalid or missing ID token.'}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        # Retrieve child data based on pk (passed in URL)
        if not pk:
            return Response({'msg': 'Child ID (pk) is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            child = Child.objects.get(id=pk)
        except Child.DoesNotExist:
            return Response({'msg': 'Child not found.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                'id': child.id,
                'name': child.name,
                'age': child.age,
                'gender': child.gender,
                'pictures': child.pictures,
                'description': child.description,
                'status': child.status,
                'comment':child.comment,
            },
            status=status.HTTP_200_OK
        )

    elif request.method == 'POST':
        # Creating a new child
        adder = Role.objects.get(id=decoded_token['uid'])
        photos = request.FILES.getlist('photos')
        photos_url = []
        for photo in photos:
            photos_url.append(upload(photo))
        
        try:
            child = Child.objects.create(
                name=request.data['name'],
                age=request.data['age'],
                gender=request.data['gender'],
                pictures=photos_url,
                description=request.data['description'],
                adder=adder,
            )
        except Exception as e:
            return Response({'msg': f'Error creating child: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {'msg': 'Child created successfully'},
            status=status.HTTP_201_CREATED
        )

    elif request.method == 'PATCH':
        # Update an existing child record based on pk (passed in URL)
        if not pk:
            return Response({'msg': 'Child ID (pk) is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            child = Child.objects.get(id=pk)
        except Child.DoesNotExist:
            return Response({'msg': 'Child not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Update fields with provided data
        if 'name' in request.data:
            child.name = request.data['name']
        if 'age' in request.data:
            child.age = request.data['age']
        if 'gender' in request.data:
            child.gender = request.data['gender']
        if 'pictures' in request.data:
            pictures = request.data['pictures']
            # Ensure pictures is a valid list of URLs
            if not isinstance(pictures, list) or not all(isinstance(url, str) and url.startswith('http') for url in pictures):
                return Response({'msg': 'Pictures must be a list of valid URLs.'}, status=status.HTTP_400_BAD_REQUEST)
            child.pictures = pictures  # Update the pictures field
        if 'description' in request.data:
            child.description = request.data['description']
        if 'comment' in request.data:
            child.comment = request.data['comment']    
        if 'status' in request.data:
            child.status = request.data['status']

        # Save the updated child object
        child.save()

        return Response(
            {'msg': 'Child updated successfully', 'id': child.id},
            status=status.HTTP_200_OK
        )

    return Response({'msg': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def get_children_by_user(request):
    print("Reached")
    try:
        # Extracting the Firebase ID token from the Authorization header
        id_token = request.headers.get('Authorization').split(" ")[1]
        decoded_token = auth.verify_id_token(id_token)
        adder = Role.objects.get(id=decoded_token['uid'])
        # Filter children by the 'adder' field using the uid from the decoded token
        if adder.role == 'parent':
            children = Child.objects.filter(adder=adder.id)
        elif adder.role == 'doctor':
            children = Child.objects.all()    
        if not children:
            return Response({'msg': 'No children found for this adder.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the child data into a list of dictionaries
        child_data = [
            {
                'id': child.id,
                'name': child.name,
                'age': child.age,
                'gender': child.gender,
                'pictures': child.pictures,  # Assuming pictures is a list of URLs
                'comment':child.comment,
                'description': child.description,
                'status': child.status,
            }
            for child in children
        ]
        
        return Response(child_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'msg': f'Error retrieving children: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_all_children(request):
    try:
        # Extracting the Firebase ID token from the Authorization header
        id_token = request.headers.get('Authorization').split(" ")[1]
        decoded_token = auth.verify_id_token(id_token)
        
        # Filter children by the 'adder' field using the uid from the decoded token
        children = Child.objects.all()
        
        if not children:
            return Response({'msg': 'No children found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the child data into a list of dictionaries
        child_data = [
            {
                'id': child.id,
                'name': child.name,
                'age': child.age,
                'gender': child.gender,
                'pictures': child.pictures,  # Assuming pictures is a list of URLs
                'description': child.description,
                'status': child.status
            }
            for child in children
        ]
        
        return Response(child_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'msg': f'Error retrieving children: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)