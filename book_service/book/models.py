from django.db import models


class Author(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)


class Book(models.Model):
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
