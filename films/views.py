from rest_framework.decorators import api_view
from rest_framework.response import Response
from films.models import Film
from films.serializers import FilmSerializers
from rest_framework import status


@api_view(['GET', 'POST'])
def film_list_api_view(request):
    if request.method == 'GET':
        # Step 1: collect data
        films = Film.objects.select_related('director')\
            .prefetch_related('genres', 'reviews').all()

        # Step 2: convert data to dict
        films_json = FilmSerializers(films, many=True).data

        # Step 3: return dict as json
        return Response(data=films_json)

    # Получение данных от клиента
    elif request.method == 'POST':
        # Step 1: Get data from body request
        title = request.data.get('title')
        text = request.data.get('text')
        duration = request.data.get('duration')
        rating = request.data.get('rating')
        director_id = request.data.get('director_id')
        genres = request.data.get('genres')

        # Step 2: Create Film with data
        film = Film.objects.create(title=title, text=text, duration=duration,
                                   rating_kinopoisk=rating, director_id=director_id)
        film.genres.set(genres)
        film.save()

        # Step 3: Return response (status) as created objects
        return Response(status=status.HTTP_201_CREATED,
                        data={'id': film.id, 'title': film.title})


# Для получения одного объекта
@api_view(['GET', 'PUT', 'DELETE'])
def film_detail_api_view(request, film_id):
    try:
        film = Film.objects.get(id=film_id)
    except Film.DoesNotExist:
        return Response(data={'message': 'Film not Found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET': # для изменения
        film_json = FilmSerializers(film, many=False).data
        return Response(data=film_json)
    elif request.method == 'PUT':
        film.title = request.data.get('title')
        film.text = request.data.get('text')
        film.duration = request.data.get('duration')
        film.rating_kinopoisk = request.data.get('rating')
        film.director_id = request.data.get('director_id')
        film.genres.set(request.data.get('genres'))
        film.save()
        return Response(status=status.HTTP_201_CREATED,
                        data={'message': 'Film update!'})
    elif request.method == 'DELETE':
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': 'Film Destroyed'})


