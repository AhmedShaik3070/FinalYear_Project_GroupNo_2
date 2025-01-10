from rest_framework.decorators import api_view
from rest_framework.response import Response
import firebase_admin
from firebase_admin import auth, credentials
from django.conf import settings
from .models import Role

if not firebase_admin._apps:
    cred = credentials.Certificate('account/serviceAccountKey.json') 
    firebase_admin.initialize_app(cred)

@api_view(['POST'])
def login(request):
    try:
        id_token = request.headers.get('Authorization').split(" ")[1]  
        decoded_token = auth.verify_id_token(id_token)
        user = auth.get_user(decoded_token['uid'])
        role = Role.objects.get(id=decoded_token['uid'])
        return Response({
            "msg": "Logged in successfully",
            "user": user.email,
            "role": role.role,
        }, status=200)

    except Exception as e:
        return Response({"msg": f"Invalid ID token, {str(e)}"}, status=401)

@api_view(['POST'])
def register(request):
    try:
        id_token = request.headers.get('Authorization').split(" ")[1]  
        
        decoded_token = auth.verify_id_token(id_token)
        id = decoded_token['uid']
        role = request.data['role']
        user = Role.objects.create(id=id,role=role)
        return Response({
            "msg": "Successfully registered the user",
        }, status=201)

    except:
        return Response({"msg": "Invalid ID token"}, status=401)    
    
