from django.shortcuts import render, redirect
from .forms import CustomerForm, AuthorForm, LoginForm
from django.contrib import auth
# Create your views here.


def register_author(request):
    if request.method == 'POST':
        form1 = CustomerForm(request.POST)
        form2 = AuthorForm(request.POST)

        if form1.is_valid() and form2.is_valid():
            instance1 = form1.save(commit=True)
            instance2 = form2.save(commit=False)
            instance2.user = instance1
            instance2.save()
            return redirect('login')

    else:
        form1 = CustomerForm()
        form2 = AuthorForm()

    context = {'form1': form1, 'form2': form2, 'title': 'Author Registration', 'spl': True}
    return render(request, 'auth/register.html', context=context)


def register_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('login')
            # print(form.cleaned_data)
    else:
        form = CustomerForm()

    context = {'form': form, 'title': 'Customer Registration', }
    return render(request, 'auth/register.html', context=context)


def login(request):
    context = {}
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = auth.authenticate(username=u, password=p)
            auth.login(request, user)
            # query = Author.objects.get(user=user)
            # if query is not None:
            #     print('query is here')
            return redirect('my_profile')

    else:
        form = LoginForm()

    context = {'form': form, 'title': 'Login', }
    return render(request, 'auth/login.html', context=context)


def logout(request):
    auth.logout(request)
    return redirect('home')
