from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path('',views.ListCourse.as_view(),name = 'List_Course'),
    path('<int:pk>/',views.RetrieveUpdateDestroyCourse.as_view(), name = 'Modify_Course'),
    path('<int:course_pk>/reviews/',views.ListReview.as_view(), name = 'List_Review'),
    path('<int:course_pk>/reviews/<int:pk>/',views.RetrieveUpdateDestroyReview.as_view(), name = 'Modify_Review'),

]
