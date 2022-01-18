from rest_framework import serializers

from .models import Movie, Review, Rating, Actor, Genre


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


class ActorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ("id", "title", "tagline", "category", "poster")


class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id", "name", "text")

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"

class MovieDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = ActorSerializer(read_only=True, many=True)
    actors = ActorSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("star", "movie")

    def validate_star(self, star):
        if star not in range(1, 6):
            raise serializers.ValidationError('Рейтинг должен быть от 1 до 5')
        return star

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating