from django.db import models
from django.conf import settings
from django.utils.text import slugify

"""
Django ORM Model for Sql/ I am using built in Sqlite3
Found in settings.py at root folder level
"""


class TestCase(models.Model):
    """ This model contains data for single test case"""

    title = models.CharField(max_length=50)
    description = models.TextField(max_length=255)
    slug = models.SlugField(max_length=100, allow_unicode=True, blank=True)

    def __str__(self):
        return self.title

    """ Create auto slug """

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(TestCase, self).save(*args, **kwargs)


class TestSuiteItem(models.Model):
    """A model that contains data for test case in our test suite"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    added = models.BooleanField(default=False)
    testcase = models.ForeignKey(TestCase, on_delete=models.CASCADE)


class TestSuites(models.Model):
    """ A model that contains list of all test cases"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    testcases = models.ManyToManyField(TestSuiteItem)
    start_date = models.DateTimeField(auto_now_add=True)
    added = models.BooleanField(default=False)
