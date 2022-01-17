from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Movie, Actor, Genre, Favorites, Likes
from .permissions import IsAdmin
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer, GenreSerializer,
)
from .service import MovieFilter

class MovieViewSet(ReadOnlyModelViewSet):
    """Список фильмов"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.all()
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == "retrieve":
            return MovieDetailSerializer

class FavoriteViewSet(ModelViewSet):
    queryset = Movie.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'add_to_favorites', 'remove_from_favorites']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return []

    @action(['POST'], detail=True)
    def add_to_favorites(self, request, pk=None):
        movie = self.get_object()
        if request.user.added_to_favorites.filter(movie=movie).exists():
            return Response('Уже добавлено в избранное')
        Favorites.objects.create(movie=movie, user=request.user)
        return Response('Добавлено в избранное')

    @action(['POST'], detail=True)
    def remove_from_favorites(self, request, pk=None):
        movie = self.get_object()
        if not request.user.added_to_favorites.filter(movie=movie).exists():
            return Response('Фильм не находится в списке избранных')
        request.user.added_to_favorites.filter(movie=movie).delete()
        return Response('Фильм удален из избранных')

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        movie = self.get_object()
        if request.user.liked.filter(movie=movie).exists():
            request.user.liked.filter(movie=movie).delete()
            return Response('False')
        else:
            Likes.objects.create(movie=movie, user=request.user)
            return Response('True')

class ReviewCreateViewSet(ModelViewSet):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer
    permission_classes = [IsAuthenticated]


class AddStarRatingViewSet(ModelViewSet):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class ActorsViewSet(ReadOnlyModelViewSet):
    """Вывод актеров или режиссеров"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == "retrieve":
            return ActorDetailSerializer

class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdmin]
