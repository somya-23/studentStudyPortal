import requests
import wikipedia
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic
from youtubesearchpython import VideosSearch

from .forms import *


# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html', {})


@login_required()
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            user = Notes(user=request.user, Title=request.POST['Title'], Description=request.POST['Description'])
            user.save()
            messages.success(request, f"Notes added from {request.user.username} successfully!")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, "form": form}
    return render(request, 'dashboard/notes.html', context)


@login_required()
def deleteNotes(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')


class NotesDetailView(generic.DetailView):
    model = Notes


@login_required()
def homeWork(request):
    if request.method == "POST":
        form = HomeWorkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['status']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = HomeWork(user=request.user,
                                 subject=request.POST['subject'],
                                 title=request.POST['title'],
                                 description=request.POST['description'],
                                 due=request.POST['due'],
                                 status=finished
                                 )
            homeworks.save()
            messages.success(request, f"Homework added from {request.user.username} successfully")
    else:
        form = HomeWorkForm()
    homework = HomeWork.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    return render(request, 'dashboard/homework.html',
                  {'homeworks': homework, 'form': form, 'homeworks_done': homework_done})


@login_required()
def update_homework(request, pk=None):
    homework = HomeWork.objects.get(id=pk)
    if homework.status == True:
        homework.status = False
    else:
        homework.status = True
    homework.save()
    return redirect('homework/')


@login_required()
def delete_homework(request, pk=None):
    t = HomeWork.objects.get(id=pk)
    t.delete()
    return redirect('homework')


def youtube(request):
    if request.method == "POST":
        form = DashBoardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input': text,
                'title': i['title'],
                'duration': i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel': i['channel']['name'],
                'link': i['link'],
                'views': i['viewCount']['short'],
                'published': i['publishedTime']
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'dashboard/youtube.html', context)
    else:
        form = DashBoardForm()
    context = {'form': form}
    return render(request, 'dashboard/youtube.html', context)


@login_required()
def todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['status']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = ToDo(
                user=request.user,
                title=request.POST['title'],
                status=finished
            )
            todos.save()
            messages.success(request, f"Todo added from {request.user.username} successfully!!")
    else:
        form = TodoForm()
    todo_list = ToDo.objects.filter(user=request.user)
    if len(todo_list) == 0:
        todos_done = True
    else:
        todos_done = False
    context = {
        'form': form,
        'todos': todo_list,
        'todos_done': todos_done
    }
    return render(request, 'dashboard/todo.html', context)


@login_required()
def update_todo(request, pk=None):
    todos = ToDo.objects.get(id=pk)
    # print(todos.status)
    if todos.status == True:
        todos.status = False
    else:
        todos.status = True
    todos.save()
    return redirect('todo')


@login_required()
def delete_todo(request, pk=None):
    ToDo.objects.get(id=pk).delete()
    return redirect('todo')


def books(request):
    if request.method == "POST":
        form = DashBoardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink'),

            }
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'dashboard/books.html', context)
    else:
        form = DashBoardForm()
    context = {'form': form}
    return render(request, 'dashboard/books.html', context)


def dictionary(request):
    if request.method == "POST":
        form = DashBoardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/" + text
        r = requests.get(url)
        answer = r.json()
        print(answer)
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            print("phoetics_somya" + phonetics)
            audio = answer[0]['phonetics'][1]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            # example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['synonyms']
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                # 'example': example,
                'synonyms': synonyms
            }
        except:
            context = {
                'form': form,
                'input': ""
            }
        print(context)

        return render(request, "dashboard/dictionary.html", context)
    else:
        form = DashBoardForm()
        context = {'form': form}
    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashBoardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary,
        }
        return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashBoardForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/wiki.html', context)


def Conversion(request):
    if request.method == "POST":
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input} yard = {int(input) * 3} foot'
                    if first == 'foot' and second == 'yard':
                        answer = f'{input} foot = {int(input) / 3} yard'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }
        if request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm()
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input = request.POST['input']
                answer = ''
                if input and int(input) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input} pound = {int(input) * 0.453592} kilogram'
                    if first == 'kilogram' and second == 'pound':
                        answer = f'{input} kilogram = {int(input) * 2.20462} pound'
                context = {
                    'form': form,
                    'm_form': measurement_form,
                    'input': True,
                    'answer': answer
                }
    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
        }
    return render(request, 'dashboard/conversion.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!!")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/register.html', context)


@login_required()
def profile(request):
    homeworks = HomeWork.objects.filter(status=False, user=request.user)
    todos = ToDo.objects.filter(status=False, user=request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todo_done = True
    else:
        todo_done = False
    context = {
        'homeworks': homeworks,
        'todos': todos,
        'homework_done': homework_done,
        'todo_done': todo_done,
    }

    return render(request, 'dashboard/profile.html', context)
