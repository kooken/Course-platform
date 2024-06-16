from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework import viewsets, generics
from rest_framework.response import Response

from course.models import Course, Lesson
from course.serializers import CourseSerializer, LessonSerializer


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Course.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CourseSerializer(Course)
        return Response(serializer.data)



class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class MotoListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class MotoRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class MotoUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class MotoDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
