from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.

def home(request):
    context = {
        "korean": Korean.objects.all(),
        "english": English.objects.all()
    }
    return render(request, "language_app/home.html", context)

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['pw'].encode('utf-8'), bcrypt.gensalt())
        new_user = User.objects.create(username=request.POST['username'], password=hashed_pw.decode('utf-8'))
        request.session['user_id'] = new_user.id
        messages.success(request, "Successfully registered!")
        return redirect('/all_translations')


def login(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        this_user = User.objects.filter(username=request.POST['username2'])
        if len(this_user) > 0:
            request.session['user_id'] = this_user[0].id
            messages.success(request, "Login successful!")
            return redirect('/all_translations')

def logout(request):
    request.session.clear()
    return redirect('/')


def translations(request):
    if 'user_id' in request.session:
        context={
            "logged_in_user": User.objects.get(id=request.session['user_id']),
            "korean": Korean.objects.all(),
            "english": English.objects.all()
        }
        return render(request, "language_app/translations.html", context)
    else:
        return redirect('/')

def addTranslation(request):
    if 'user_id' in request.session:
        context= {
            "logged_in_user": User.objects.get(id=request.session['user_id'])
        }
        return render(request, "language_app/add_translation.html", context)
    else:
        return redirect('/')

def submitTranslation(request):
    errors = Korean.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key,value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/add_translation')
    else:
        eng = English.objects.filter(english=request.POST['english'])
        if len(eng) > 0:
            add_eng = English.objects.get(english=request.POST['english'])
            Korean.objects.create(korean = request.POST['korean'], politeness_level = request.POST['politeness_level'], eng_translation = add_eng, uploaded_by=User.objects.get(id=request.session['user_id']))
        else:
            new_eng = English.objects.create(english = request.POST['english'])
            Korean.objects.create(korean = request.POST['korean'], politeness_level = request.POST['politeness_level'], eng_translation = new_eng, uploaded_by=User.objects.get(id=request.session['user_id']))
        messages.success(request, "Translation successfully added")
        return redirect('/all_translations')

def deleteTranslation(request):
    Korean.objects.get(id=request.POST['korean_id']).delete()
    return redirect('/all_translations')