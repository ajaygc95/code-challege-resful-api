from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from django.utils import timezone
from .serializers import (
    TestCaseSerializer,
    TestSuitesSerializer,
    TestSuiteItemSerializer,
    UserSerializer)
from django.contrib.auth.models import User
from rest_framework.generics import RetrieveAPIView
from .models import TestCase, TestSuites, TestSuiteItem
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TestCaseView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TestCaseSerializer
    queryset = TestCase.objects.all()

    def post(self, request, *args, **kwargs):
        """
        post api request from the user endpoint
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        description = request.data['description']
        title = request.data['title']

        TestCase.objects.create(title=title, description=description)
        return Response({'message': "created"}, status=200)


class TestSuitesView(viewsets.ModelViewSet):
    """
    API endpoint that allows test Suite to be viewed or edited.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TestSuitesSerializer
    queryset = TestSuites.objects.all()
    lookup_field = 'slug'

    def post(self, request, *args, **kwargs):
        """
        create method overloaded for Test Suite List
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        slug = self.kwargs['slug']
        user = request.user
        testcase = get_object_or_404(TestCase, slug=slug)
        testcaseitem, created = TestSuiteItem.objects.get_or_create(
            testcase=testcase,
            user=user,
            added=False
        )
        test_suite_qs = TestSuites.objects.filter(
            user=user,
        )
        if test_suite_qs.exists():
            testsuite = test_suite_qs[0]

            # check if the test case is in the test suite
            if testsuite.testcases.filter(testcase__slug=testcase.slug).exists():
                return Response({'message': "Test case is already in the suite"}, status=200)
            else:
                testsuite.testcases.add(testcaseitem)
                return Response({'message': "Test case has been appended to the Test Suite list"}, status=200)
        else:
            testsuite = TestSuites.objects.create(user=user, start_date=timezone.now())
            testsuite.testcases.add(testcaseitem)
            return Response({'message': "Test case has been added to Test Suite"}, status=200)


    def destroy(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        user = request.user
        testcase = get_object_or_404(TestCase, slug=slug)
        test_suite_qs = TestSuites.objects.filter(
            user=user,
        )
        if test_suite_qs.exists():
            testsuite = test_suite_qs[0]
            # check if the test case is in the test suite
            if testsuite.testcases.filter(testcase__slug=testcase.slug).exists():
                testcaseitem = TestSuiteItem.objects.filter(
                    testcase = testcase,
                    user = user,
                    added = False
                )[0]
                testsuite.testcases.remove(testcaseitem)
                return Response({'message': "Test case has been removed from the test suite"}, status=200)
            else:
                return Response({'message': "There is no test case in the suite with that name"}, status=200)
        else:
            return Response({'message': "There is no active Test Suite"}, status=200)


class GetTestSuiteItem(viewsets.ModelViewSet):
    serializer_class = TestSuiteItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = TestSuiteItem.objects.all()