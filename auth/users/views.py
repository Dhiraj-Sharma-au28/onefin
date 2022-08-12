from unittest import result
from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer,MoviesSerializer
from .models import User,Movies
import jwt,datetime
import requests


# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        

class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({'error':'User not found!'})
        if not user.check_password(password):
            return Response({'error':'Password is incorrect!'})
        
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1)
            
            
        }
        token = jwt.encode(payload,'secret',algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data = {'token':token}

        
        return response

class UserView(APIView):

    def get(self,request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            return Response({'error':'you are not logged in'})
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except:
            return Response({'error':'invalid token'})
        
        
        result = []
        movies = Movies.objects.all()
        for movie in movies:
            result.append({

                
                'title':movie.title,
                'description':movie.description,
                "Movies":[{
                    'movieTitle':movie.movieTitle,
                    'movieDescription':movie.movieDescription,
                    'movieGenre':movie.movieGenre,
                    'id':movie.id,
                }]
                
            })
        
        return Response(result)


    def post(self,request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            return Response({'error':'you are not logged in'})
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except:
            return Response({'error':'invalid token'})
        
        
        serializer = MoviesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"id":serializer.data['id']})

    def put(self,request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            return Response({'error':'you are not logged in'})
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except:
            return Response({'error':'invalid token'})
        
        
        key  = request.query_params['id']
        movie = Movies.objects.get(id=key)
        serializer = MoviesSerializer(movie,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self,request):

        token = request.COOKIES.get('jwt')
        
        if not token:
            return Response({'error':'you are not logged in'})
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except:
            return Response({'error':'invalid token'})
        
        
        key  = request.query_params['id']
        movie = Movies.objects.get(id=key)
        movie.delete()
        return Response({"id":key})

class MoviesView(APIView):
    
    def get(self,request):

        Username = 'iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0'
        Password = 'Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1'

        body_Username = request.data['Username']
        body_Password = request.data['Password']

        if Username == body_Username and Password == body_Password:
            r = requests.get(' https://demo.credy.in/api/v1/maya/movies/')
            return Response(r.json())
        
        else:
            return Response({'error':'invalid credentials!Please try again'})

        
        
