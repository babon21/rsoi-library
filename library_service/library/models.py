from django.db import models


class Library(models.Model):
    city = models.CharField(max_length=255, blank=True)


class LibraryBook(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    book_id = models.BigIntegerField()
    count = models.IntegerField()


class TakenBook(models.Model):
    book_id = models.BigIntegerField()
    user_id = models.BigIntegerField()
    date = models.DateTimeField(auto_now=True)
    expire_date = models.DateTimeField(auto_now=False)
