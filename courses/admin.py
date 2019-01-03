from django.contrib import admin
from .models import Course, Chapter, Section, Enroll, Author

admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Section)
admin.site.register(Enroll)
admin.site.register(Author)