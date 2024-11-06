from rest_framework import serializers
from films.models import Film


class FilmSerializers(serializers.ModelSerializer):
    class Meta:
        model = Film
        # fields = ['id', 'title', 'duration']
        fields = '__all__'
#         exclude = ['id'] # Исключает id и выводит все остальное


