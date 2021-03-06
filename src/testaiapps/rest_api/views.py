from django.shortcuts import redirect
from rest_framework import viewsets, permissions
from django.utils import timezone
from .serializers import (
    TestCaseSerializer,
    TestSuitesSerializer,
    TestSuiteItemSerializer,
    MergeTwoSerializer,
    UserSerializer)
from django.contrib.auth.models import User
from rest_framework.generics import RetrieveAPIView
from .models import TestCase, TestSuites, TestSuiteItem
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework import mixins, viewsets
from django.http import HttpResponse


def home(request):
    """ Home page renderer... """
    return render(request,"rest_api/index.html")


class UserViewSet(viewsets.ModelViewSet):
    """Get User Detail """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TestCaseView(viewsets.ModelViewSet):
    """CRUD functionlity for individual test case"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TestCaseSerializer
    queryset = TestCase.objects.all()

    def post(self, request, *args, **kwargs):
        """
        overriding create functionality for modelviewset
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        description = request.data['description']
        title = request.data['title']

        TestCase.objects.create(title=title, description=description)
        return Response({'message': "created"}, status=200)

class TestSuiteItemView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TestSuiteItemSerializer
    queryset = TestSuiteItem.objects.all()

class TestSuitesView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TestSuitesSerializer
    queryset = TestSuites.objects.all()

    def update(self, request, *args, **kwargs):
        getPK = self.kwargs['pk']
        slug = request.data['testcases']
        user = request.user

        testcase = get_object_or_404(TestCase, slug=slug)
        print(testcase)
        testcaseitem, created = TestSuiteItem.objects.get_or_create(
            testcase=testcase,
            user=request.user,
            added=False
        )
        print(testcaseitem)
        test_suite_qs = TestSuites.objects.filter(pk=getPK)
        print(test_suite_qs)

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


class GetTestSuiteItem(viewsets.ModelViewSet):
    """
    Queryset for the retrieving individual test cases info
    """
    serializer_class = TestSuitesSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = TestSuites.objects.all()

    # queryset = None

    def retrieve(self, request, *args, **kwargs):
        get_pk = self.kwargs['pk']
        test_suite_qs = TestSuites.objects.filter(pk=get_pk)

        if test_suite_qs.exists():
            testsuite = test_suite_qs[0]
            single_test_case = testsuite.testcases.all()

            context = {}
            for item in single_test_case:
                wrapper_context = {}
                wrapper_context['id'] = item.testcase.id
                wrapper_context['title'] = item.testcase.title
                wrapper_context['slug'] = item.testcase.slug
                wrapper_context['description'] = item.testcase.description

                context[item.testcase.slug] = wrapper_context
            return Response(context)
        else:
            return Response({"message": "There is no such test suite or no items in the test suite"})


class MergeTwoCasesView(viewsets.ModelViewSet):
    """Merge Two test cases View"""
    serializer_class = MergeTwoSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = TestSuites.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        Merge is done jsut to merge two test cases and suplly with
        json restful.
        response is combined title and single json with two test cases.

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        print(self.request.data)
        get_pk = self.kwargs['pk']

        requestdata = self.request.data
        dict1 = dict(requestdata)
        slug1 = str(dict1['firstcase'][0]).lower()
        slug2 = str(dict1['secondcase'][0]).lower()

        testcase1 = get_object_or_404(TestCase, slug=slug1)
        testcase2 = get_object_or_404(TestCase, slug=slug2)
        test_suite_qs = TestSuites.objects.filter(pk=get_pk)
        if test_suite_qs.exists():
            testsuite = test_suite_qs[0]
            single_test_case = testsuite.testcases.all()

            tests1_in_suite = False
            tests2_in_suite = False

            mergetitle = f"{testcase1}{testcase2}"
            context = {mergetitle:{}}

            for item in single_test_case:
                itemid = str(item.testcase.slug).lower()
                if itemid == slug1:
                    print(itemid, testcase1)
                    wrapper_context = {'id': item.testcase.id, 'title': item.testcase.title, 'slug': item.testcase.slug,
                                       'description': item.testcase.description}
                    context[mergetitle][item.testcase.slug] = wrapper_context

                if itemid == slug2:
                    print(itemid, testcase2)
                    wrapper_context = {'id': item.testcase.id, 'title': item.testcase.title, 'slug': item.testcase.slug,
                                       'description': item.testcase.description}
                    context[mergetitle][item.testcase.slug] = wrapper_context
            return Response(context)
        else:
            return Response({"message": "There is no such test suite or no items in the test suite"})
