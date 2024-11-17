from rest_framework.decorators import api_view
from rest_framework.response import Response
from films.models import Film, Director, Genre
from films.serializers import FilmSerializers, FilmCreateValidateSerializers, \
    DirectorSerializers, GenreSerializers
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class FilmListCreateAPIView(ListCreateAPIView):
    serializer_class = FilmSerializers
    queryset = Film.objects.all()
    pagination_class = PageNumberPagination

# класс basequery
    def post(self, request, *args, **kwargs):
        serializer = FilmCreateValidateSerializers(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'Request failed', 'errors': serializer.errors})

        genres = serializer.validated_data.get('genres')

        film = Film.objects.create(**serializer.create_validated_data())
        film.genres.set(genres)
        film.save()

        return Response(status=status.HTTP_201_CREATED,
                        data={'id': film.id, 'title': film.title})


class GenreAPIViewSet(ModelViewSet):
    serializer_class = GenreSerializers
    queryset = Genre.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = 'id'


class DirectorListCreateAPIView(ListCreateAPIView):
    serializer_class = DirectorSerializers
    queryset = Director.objects.all()
    pagination_class = PageNumberPagination


class DirectorDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DirectorSerializers
    queryset = Director.objects.all()
    lookup_field = 'id'


@api_view(['GET', 'POST'])
def film_list_api_view(request):
    print(request.user)
    if request.method == 'GET':
        # Step 1: collect data
        films = Film.objects.select_related('director')\
            .prefetch_related('genres', 'reviews').all()

        # Step 2: convert data to dict
        films_json = FilmSerializers(instance=films, many=True).data

        # Step 3: return dict as json
        return Response(data=films_json)

    # Получение данных от клиента
    # elif request.method == 'POST':


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
        serializer = FilmCreateValidateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True) # Упрощенная версия 24 по 27 строчки кода
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


