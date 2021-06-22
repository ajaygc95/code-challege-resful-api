from django.contrib import admin

# Register your models here.
from .models import TestCase, TestSuiteItem, TestSuites


class TestCasesAdmin(admin.ModelAdmin):
    model = TestCase


admin.site.register(TestCase, TestCasesAdmin)
admin.site.register(TestSuites)
admin.site.register(TestSuiteItem)
