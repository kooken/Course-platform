from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from course.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.course = Course.objects.create(title="Web dev", description="Brand new course on web dev")
        self.lesson = Lesson.objects.create(description="First lesson. Introduction.", course=self.course,
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("course:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), self.lesson.title
        )

    def test_lesson_create(self):
        url = reverse("course:lessons_create")
        data = {
            "description": "Second lesson. Fundamentals."
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.filter(description="Second lesson. Fundamentals.").count(), 1
        )

    def test_lesson_update(self):
        url = reverse("course:lessons_update", args=(self.lesson.pk,))
        data = {
            "description": "Second lesson. Not only fundamentals."
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("description"), "Second lesson. Not only fundamentals."
        )

    def test_lesson_delete(self):
        url = reverse("course:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse("course:lessons_list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        result = {
                  "count": 1,
                  "next": None,
                  "previous": None,
                  "results": [
                             {
                              "id": self.lesson.pk,
                              "description": self.lesson.description,
                              "preview": None,
                              "link": None,
                              "course": self.course.pk}
                              ]
                }
        self.assertEqual(
            data, result
        )


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.course = Course.objects.create(title="Swift", description="iOS development", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        url = reverse("course:course_subscription")
        data = {"course": self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {"message": "Subscription enabled"})

    def test_unsubscribe(self):
        url = reverse("course:course_subscription")
        data = {"course": self.course.pk}
        Subscription.objects.create(course=self.course, user=self.user)
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, {'message': 'Subscription disabled'})
