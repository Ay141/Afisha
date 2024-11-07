from rest_framework import serializers
from films.models import Film, Director, Review


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


