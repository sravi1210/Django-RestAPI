# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
#
# from . import models
# from . import serializers
#
# class ListCourse(APIView):
#     def get(self, request, format = None):
#         courses = models.Course.objects.all()
#         serializer = serializers.CourseSerializer(courses, many = True)
#         return Response(serializer.data)
#
#     def post(self, request, format = None):
#          serializer = serializers.CourseSerializer(data = request.data)
#          serializer.is_valid(raise_exception = True)
#          serializer.save()
#          return Response(serializer.data, status=status.HTTP_201_CREATED)


from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework import permissions

from . import models
from . import serializers

class ListCourse (generics.ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer


class RetrieveUpdateDestroyCourse(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer


class ListReview (generics.ListCreateAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return self.queryset.filter(course_id = self.kwargs.get('course_pk'))

    def perform_create(self, serializer):
        course = get_object_or_404(models.Course, pk = self.kwargs.get('course_pk'))
        serializer.save(course=course)


class RetrieveUpdateDestroyReview(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def get_object(self):
        return get_object_or_404(self.get_queryset(),
                                course_id = self.kwargs.get('course_pk'),
                                pk = self.kwargs.get('pk')
                                )

#this method is used for version control on the api

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser :
            return True
        elif request.method == 'DELETE' :
            return False
        return True

class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = (
                            IsSuperUser,
                            permissions.DjangoModelPermissions,
                        ) #for this view set ignore default permission and check for this

    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

    @action(detail = True, methods=['get'])
    def reviews(self, request, pk=None):
        self.pagination_class.page_size = 1 #custom method to set page size in adhoc methods
        reviews = models.Review.objects.all().filter(course_id = pk)

        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = serializers.ReviewSerializer(page, many= True)
            return self.get_paginated_response(serializer.data)





        course = self.get_object()
        review =  course.reviews.all()
        # or
        # review = models.Review.objects.all().filter(course_id = pk)

        serializer = serializers.ReviewSerializer(review, many = True)
        return Response(serializer.data)

class ReviewViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet
                  ):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

# class ReviewViewSet(viewsets.ModelViewSet):
#     queryset = models.Review.objects.all()
#     serializer_class = serializers.ReviewSerializer
