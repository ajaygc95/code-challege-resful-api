from django.urls import path, include
from . import views
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

"""
Using routter from django rest framework.
Overidden in django/views

"""
router = routers.DefaultRouter()
router.register(r'testcases', views.TestCaseView, 'testcases')
router.register(r'users', views.UserViewSet, 'users')
router.register(r'test_suite_cases', views.TestSuitesView, 'testsuite_cases')
router.register(r'merge_two_test', views.MergeTwoCasesView, 'merge_two_Test')
router.register(r'get_suite_items', views.GetTestSuiteItem, 'get_suite_items')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.home, name="default-home"),
]
""" This for media CRUD functionality if needed """
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
