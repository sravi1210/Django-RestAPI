from rest_framework import serializers
from django.db.models import Avg
from . import models

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'email' : {'write_only' : True}
        }
        fields = (
            'id',
            'course',
            'name',
            'email',
            'comment',
            'rating',
            'created_at'
        )
        model = models.Review

class CourseSerializer(serializers.ModelSerializer):
    # for one to many relationship between course and review
    # reviews = ReviewSerializer(many = True, read_only = True)

    #instead of this displaying whole data their with the courses we can display it as a hyperlink to a page containing that RetrieveUpdateDestroyAPIView
    # reviews = serializers.HyperlinkedRelatedField(
    #         many = True,
    #         read_only = True,
    #         view_name = 'apiv2:review-detail'
    # )
    #instead you can use the primary key method to just diplay pk's of reviews there
    reviews = serializers.PrimaryKeyRelatedField(
            many = True,
            read_only = True,
    )

    average_rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'title',
            'url',
            'reviews',
            'average_rating',
        )
        model = models.Course

    def get_average_rating(self, obj):   #name is special get_fieldname
        average  = obj.reviews.aggregate(Avg('rating')).get('rating__avg')

        if average is None:
            return 0

        return round(average*2) / 2
