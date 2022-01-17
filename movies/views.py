from django.db import models
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Movie, Actor, Genre, Favorites
from .permissions import IsAdmin
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer,
    ActorDetailSerializer, GenreSerializer,
)
from .service import get_client_ip, MovieFilter

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Список фильмов"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.all().annotate(
            rating_user=models.Count("ratings",
                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
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
        if request.user.liked.filter(movie=movie).exists():
            return Response('Уже добавлено в избранное')
        Favorites.objects.create(movie=movie, user=request.user)
        return Response('Добавлено в избранное')

    @action(['POST'], detail=True)
    def remove_from_favorites(self, request, pk=None):
        movie = self.get_object()
        if not request.user.liked.filter(movie=movie).exists():
            return Response('Фильм не находится в списке избранных')
        request.user.liked.filter(movie=movie).delete()
        return Response('Фильм удален из избранных')

class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
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
