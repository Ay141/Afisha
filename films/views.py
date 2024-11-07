from rest_framework.decorators import api_view
from rest_framework.response import Response
from films.models import Film
from films.serializers import FilmSerializers
from rest_framework import status


@api_view(['GET'])
def film_list_api_view(request):
    # Step 1: collect data
    films = Film.objects.select_related('director')\
        .prefetch_related('genres', 'reviews').all()
    # Step 2: convert data to dict
    films_json = FilmSerializers(films, many=True).data
    # Step 3: return dict as json
    return Response(data=films_json)


# Для получения одного объекта
@api_view(['GET'])
def film_detail_api_view(request, film_id):
    try:
        film = Film.objects.get(id=film_id)
    except Film.DoesNotExist:
        return Response(data={'message': 'Film not Found!'},
                        status=status.HTTP_404_NOT_FOUND)
    film_json = FilmSerializers(film, many=False).data
    return Response(data=film_json)
