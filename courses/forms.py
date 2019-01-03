from django import forms
from .models import Course, Chapter, Section, Enroll
from djangoformsetjs.utils import formset_media_js

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        exclude = ('author', )


class ChapterForm(forms.ModelForm):

    class Meta:
        model = Chapter
        exclude = ('course', )


class SectionForm(forms.ModelForm):

    class Meta:
        model = Section
        fields = '__all__'

    class Media(object):
        # The form must have `formset_media_js` in its Media
        js = formset_media_js + (
            # Other form javascript...
        )


class EnrollForm(forms.ModelForm):

    class Meta:
        model = Enroll
        fields = '__all__'


SectionFormSet = forms.formset_factory(SectionForm, extra=1)
