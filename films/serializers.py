from rest_framework import serializers
from films.models import Film, Director, Review, Genre
from rest_framework.exceptions import ValidationError


class DirectorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Director
        # fields = '__all__'
        fields = 'id name year age'.split()


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text stars'.split()


class FilmSerializers(serializers.ModelSerializer):
    director = DirectorSerializers()
    genres = serializers.SerializerMethodField()
    all_reviews = ReviewSerializers(many=True) # Вывод звезды

    class Meta:
        model = Film
        fields = 'id title genres director rating_kinopoisk all_reviews reviews '.split()

    def get_genres(self, film):
        return[
            genre.title
            for genre in film.genres.all()
               ]


class FilmCreateValidateSerializers(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=4, max_length=20)
    text = serializers.CharField(required=False)
    duration = serializers.IntegerField()
    rating = serializers.FloatField(min_value=1, max_value=10)
    director_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exist!')
        return director_id

    def validate_genres(self, genres):
        genres = list(set(genres))
        genre_db = Genre.objects.filter(id__in=genres)
        if genre_db.count() != len(genres):
            raise ValidationError('Genre does not exist!')
        return genres

    def create_validated_data(self):
        validated = self.validated_data
        return {
            'title': validated['title'],
            'text': validated['text'],
            'rating_kinopoisk': validated['rating_kinopoisk'],
            'duration': validated['duration'],
            'director_id': validated['director_id']

        }