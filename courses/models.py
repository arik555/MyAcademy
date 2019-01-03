from django.db import models
from django.contrib.auth.models import User
from markdown import markdown

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=150)
    desc = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.IntegerField(blank=True)
    rating = models.FloatField(blank=True)
    avatar = models.URLField()

    def __str__(self):
        return self.name

    def beautify(self):
        return markdown(self.desc, safe_mode='escape')


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='my_chapter')
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Section(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='my_section')
    name = models.CharField(max_length=150)
    desc = models.TextField(blank=True)
    content = models.FileField(upload_to='uploads/', blank=True)

    def __str__(self):
        return self.name

    def beautify(self):
        return markdown(self.desc, safe_mode='escape')


class Enroll(models.Model):
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course, related_name='my_enroll')

    def __str__(self):
        return self.timestamp.strftime("%d %B, %Y")

