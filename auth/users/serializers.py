from pyexpat import model
from rest_framework import serializers
from .models import User,Movies


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email','password']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

        
class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ['id','title','description','movieTitle','movieDescription']
        

    
        
        