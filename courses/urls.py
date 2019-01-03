from django.urls import path, re_path
from .views import (add_chapter, add_course,
                    add_section, edit_chapter,
                    edit_course, edit_section,
                    delete_chapter, delete_course,
                    delete_section, browse, upgrade_account,
                    preview_upload_profile, ask_for_more, enroll_course)

urlpatterns = [
    path('browse/', browse, name='browse'),
    path('browse/course=<int:course>', browse, name='browse'),
    path('courses/add/', add_course, name='add_course'),
    path('courses/del/<int:id>', delete_course, name='delete_course'),
    path('courses/edit/<int:id>', edit_course, name='edit_course'),
    path('chapters/add/course=<int:course>', add_chapter, name='add_chapter'),
    path('chapters/edit/<int:id>', edit_chapter, name='edit_chapter'),
    path('chapters/delete/<int:id>', delete_chapter, name='delete_chapter'),
    path('sections/add/course=<int:course>&chapter=<int:chapter>', add_section, name='add_section'),
    path('sections/edit/<int:id>', edit_section, name='edit_section'),
    path('sections/delete/<int:id>', delete_section, name='delete_section'),
    path('upgrade_account/', upgrade_account, name='upgrade_account'),
    path('myprofile/', preview_upload_profile, name='my_profile'),
    path('more-chapters/course=<int:course>', ask_for_more, name='ask'),
    path('enroll/course<int:course>', enroll_course, name='enroll_course'),
]