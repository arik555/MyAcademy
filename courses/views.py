from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Course, Chapter, Section, Enroll, Author
from .forms import CourseForm, ChapterForm, SectionForm, EnrollForm
from django.contrib import auth
from django.forms.models import inlineformset_factory


def home(request):
    new_context = {}
    if request.user.is_authenticated:
        author = Author.objects.filter(user__exact=request.user).count()
        if author != 0:
            author = Author.objects.get(user=request.user)
            if author is not None:
                new_context = {'author': author, }
    query = Course.objects.filter(id__lte=10)
    context = {'query': query, 'title': 'Homepage', }
    context.update(new_context)
    return render(request, 'index.html', context=context)


def browse(request, course=None):
    query = Course.objects.all()
    # print('top')
    if course is None:
        if request.method == 'GET':
            # print(request.GET)
            if 'qs' in request.GET:
                search = request.GET['qs']
                # print(search)
                query = Course.objects.filter(name__contains=search)
                if query.count() == 0:
                    # print('nrf')
                    new_context = {'nrf': True, }
        else:
            query = Course.objects.all()
        new_context = {}
    else:
        if request.user.is_authenticated:
            query = Course.objects.get(id=course)
            enroll = Enroll.objects.filter(user=request.user, course=query)
            count = enroll.count()
            print(count)
            if count >= 1:
                new_context = {'enroll': enroll, 'invoke': True, }
            else:
                new_context = {'invoke': True, }
        else:
            query = Course.objects.get(id=course)
            enroll = Enroll.objects.filter(course=query)
            count = enroll.count()
            print(count)
            if count >= 1:
                new_context = {'enroll': enroll, 'invoke': True, 'login': False, }
            else:
                new_context = {'invoke': True, }
    context = {'query': query, 'title': 'Browse Courses', }
    context.update(new_context)
    print(context)
    return render(request, 'common/browse.html', context=context)


# def my_courses(request):
#     query = Course.objects.all()
#     context = {'query': query, 'title': 'Browse Courses', 'spl': True, }
#     return render(request, 'common/browse.html', context=context)


def preview_upload_profile(request):
    if request.user.is_authenticated:
        author = Author.objects.filter(user__exact=request.user).count()
        if author != 0:
            author = Author.objects.get(user=request.user)
            if author is not None:
                print('author')
                query = Course.objects.filter(author=author)
                enroll_query = Enroll.objects.filter(user=request.user)
                context = {'query': query, 'title': 'User Profile', 'auth': True, 'author': author,
                           'enroll_query': enroll_query, }
        else:
            user = auth.models.User.objects.get(username=request.user.username)
            query = Enroll.objects.filter(user=request.user)
            context = {'query': query, 'title': 'User Profile', 'auth': False, 'customer': user, }
        return render(request, 'common/profile.html', context=context)
    else:
        return redirect('login')


def add_course(request):
    if not request.user.is_authenticated:
        return redirect('login')
    author = Author.objects.filter(user__exact=request.user).count()
    print(author)
    if author == 0:
        return redirect('home')
    author = Author.objects.get(user=request.user)
    if author is None:
        # print(instance.author, author.user)
        return HttpResponse('Permission Denied!')
    if request.method == 'POST':
        form = CourseForm(request.POST)

        if form.is_valid():
            instance_carry = form.save(commit=False)
            instance_carry.author = author
            instance_carry.save()
            return redirect('add_chapter', course=instance_carry.id)

    else:
        form = CourseForm()

    context = {'form': form, 'title': 'Add Course', 'course': True, }
    return render(request, 'common/add.html', context=context)


def edit_course(request, id=id):
    if not request.user.is_authenticated:
        return redirect('home')
    author = Author.objects.filter(user__exact=request.user).count()
    if author == 0:
        return redirect('home')
    instance = get_object_or_404(Course, id=id)
    author = Author.objects.get(user=request.user)
    if author is None:
        # print(instance.author, author.user)
        return HttpResponse('Permission Denied!')
    form = CourseForm(instance=instance)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=instance)

        if form.is_valid():
            form.save(commit=True)
            return redirect('home')

    context = {'form': form, 'title': 'Edit Course', }
    return render(request, 'common/edit.html', context=context)


def delete_course(request, id=id):
    if not request.user.is_authenticated:
        return redirect('home')
    author = Author.objects.filter(user__exact=request.user).count()
    if author == 0:
        return redirect('home')
    author = Author.objects.get(user=request.user)
    if author is None:
        # print(instance.author, author.user)
        return HttpResponse('Permission Denied!')
    instance = Course.objects.get(id=id)
    instance.delete()
    return redirect('my_profile')


def add_chapter(request, course=None):
    if not request.user.is_authenticated:
        return redirect('home')
    author = Author.objects.filter(user__exact=request.user).count()
    if author == 0:
        return redirect('home')
    author = Author.objects.get(user=request.user)
    if author is None:
        # print(instance.author, author.user)
        return HttpResponse('Permission Denied!')
    form = ChapterForm(request.POST or None)
    course_select = Course.objects.get(id=course)
    if form.is_valid():
        instance_carry = form.save(commit=False)
        instance_carry.course = course_select
        instance_carry.save()
        return redirect('add_section', course=course_select.id, chapter=instance_carry.id)

    context = {'form': form, 'title': 'Add Chapter', 'chapter': True, 'course_select': course_select, }
    return render(request, 'common/add.html', context=context)


def edit_chapter(request, id=id):
    if not request.user.is_authenticated:
        return redirect('home')
    author = Author.objects.filter(user__exact=request.user).count()
    if author == 0:
        return redirect('home')
    author = Author.objects.get(user=request.user)
    if author is None:
        # print(instance.author, author.user)
        return HttpResponse('Permission Denied!')
    instance = get_object_or_404(Chapter, id=id)
    form = ChapterForm(instance=instance)
    if request.method == 'POST':
        form = ChapterForm(request.POST, instance=instance)

        if form.is_valid():
            form.save(commit=True)
            return redirect('my_profile')

    context = {'form': form, 'title': 'Edit Chapter', }
    return render(request, 'common/edit.html', context=context)


def delete_chapter(request, id=id):
    if not request.user.is_authenticated:
        return redirect('home')
    author = Author.objects.filter(user__exact=request.user).count()
    if author == 0:
        return redirect('home')
    author = Author.objects.get(user=request.user)
    if author is None:
        # print(instance.author, author.user)
        return HttpResponse('Permission Denied!')
    instance = Chapter.objects.get(id=id)
    instance.delete()
    return redirect('my_profile')


def add_section(request, course=None, chapter=None):
    if not request.user.is_authenticated:
        return redirect('home')
    author = Author.objects.filter(user__exact=request.user).count()
    if author == 0:
        return redirect('home')
    author = Author.objects.get(user=request.user)
    if author is None:
        # print(instance.author, author.user)
        return HttpResponse('Permission Denied!')
    SectionFormSet = inlineformset_factory(Chapter, Section, form=SectionForm, can_delete=True, extra=0, min_num=1,
                                           can_order=True)
    formset = SectionFormSet(request.POST or None, request.FILES or None)
    course_select = Course.objects.get(id=course)
    chapter_select = Chapter.objects.get(id=chapter)
    if formset.is_valid():
        instance_carry = formset.save(commit=False)
        print(instance_carry)
        for each in instance_carry:
            each.chapter = chapter_select
            each.save()
        return redirect('ask', course=course_select.id)

    context = {'formset': formset, 'title': 'Add Section', 'section': True, 'course_select': course_select,
               'chapter_select': chapter_select, }
    return render(request, 'common/add.html', context=context)


def edit_section(request, id=id):
    if not request.user.is_authenticated:
        return redirect('home')
    author = Author.objects.filter(user__exact=request.user).count()
    if author == 0:
        return redirect('home')
    author = Author.objects.get(user=request.user)
    if author is None:
        # print(instance.author, author.user)
        return HttpResponse('Permission Denied!')
    instance = get_object_or_404(Section, id=id)
    form = SectionForm(instance=instance)
    if request.method == 'POST':
        form = SectionForm(request.POST, instance=instance)

        if form.is_valid():
            form.save(commit=True)
            return redirect('my_profile')

    context = {'form': form, 'title': 'Edit Section', }
    return render(request, 'common/edit.html', context=context)


def delete_section(request, id=id):
    if not request.user.is_authenticated:
        return redirect('home')
    author = Author.objects.filter(user__exact=request.user).count()
    if author == 0:
        return redirect('home')
    author = Author.objects.get(user=request.user)
    if author is None:
        # print(instance.author, author.user)
        return HttpResponse('Permission Denied!')
    instance = Section.objects.get(id=id)
    instance.delete()
    return redirect('my_profile')


def ask_for_more(request, course=None):
    context = {'course_id': course, 'title': 'Add More Chapters?', 'ask': True, }
    return render(request, 'common/more.html', context=context)


def upgrade_account(request):
    if request.user.is_authenticated:
        author = Author.objects.create(user=request.user, author=True)
        author.save()
        return redirect('my_profile')
    return redirect('login')


def enroll_course(request, course=None):
    if request.user.is_authenticated:
        enroll = Enroll.objects.create(user=request.user)
        course = Course.objects.get(id=course)
        enroll.course.add(course)
        enroll.save()
        return redirect('my_profile')
    return redirect('login')