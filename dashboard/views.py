from django.shortcuts import render
from .forms import NotesForm,HomeworkForm,DashboardForm,UserRegistrationForm
from .models import Notes,Homework
from django.http import HttpResponse
from django.shortcuts import redirect
from youtubesearchpython import VideosSearch
from json.decoder import JSONDecodeError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .openai_chat import chat_with_gpt
import requests
# Create your views here. 
def home(request):
    return render(request,'dashboard/home.html')



def chat_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        bot_response = chat_with_gpt(user_message)
        return render(request, 'dashboard/chat.html', {'response': bot_response})
    return render(request, 'dashboard/chat.html')


def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            # Process the form data
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            
            # Save the note or perform any desired actions
            notes = Notes(title=title, description=description, user=request.user)
            notes.save()
            
            return HttpResponse("Note created successfully!")
    else:
        notes=Notes.objects.filter(user=request.user)
        form=NotesForm
        context={'notes': notes, 'form': form}
        return render(request,'dashboard/notes.html',context)

def delete_note(request,pk):
    note=Notes.objects.filter(id=pk).delete()
    return redirect('notes')

def homework(request):
    if request.method=='POST':
        form=HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished=True
                else:
                    fiinished=False
            except:
                finished=False
            homeworks=Homework(
                user=request.user,
                Subject=request.POST['Subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due_date=request.POST['due_date'],
                is_finished=finished,
            )
            homeworks.save()
            return HttpResponse("Note created successfully!")
    else:
        form=HomeworkForm
    homework=Homework.objects.filter(user=request.user)
    items=len(homework)

    context={'homeworks':homework, 'items':items,'form':form}
    return render(request,'dashboard/homework.html',context)


def deletehomework(request,pk):
    homework=Homework.objects.filter(id=pk).delete()
    return redirect('homework')

def youtube(request):
    if request.method == 'POST':
        form=DashboardForm(request.POST)
        text=request.POST['text']
        videos=VideosSearch(text,limit=10)
        result_list=[]
        for i in videos.result()['result']:
            result_dict={
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
                    desc+=j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
            context={'results':result_list,'form':form}
        return render(request,'dashboard/youtube.html',context)
    else:
        form=DashboardForm()
    context={'form':form} 
    return render(request,'dashboard/youtube.html',context)



def books(request):
    if request.method == 'POST':
        form=DashboardForm(request.POST)
        text=request.POST['text']
        url= "https://www.googleapis.com/books/v1/volumes?q="+text
        r=requests.get(url)
        answer=r.json()
        result_list=[]
        for i in range(10):
            result_dict={
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
                
                
               
            }
           
            result_list.append(result_dict)
            context={'results':result_list,'form':form}
        return render(request,'dashboard/books.html',context)
    else:
        form=DashboardForm()
    context={'form':form} 
    return render(request,'dashboard/books.html',context)

def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
        r = requests.get(url)
        answer = r.json()

        try:
            
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms,
            }
        except (JSONDecodeError, IndexError, KeyError):
            context = {
                'form': form,
                'input': '',
            }
        
        return render(request, "dashboard/dictionary.html", context)
    else:
        form = DashboardForm()
        context = {'form': form}
        
    return render(request, 'dashboard/dictionary.html', context)


def register(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            return redirect('login')
    else:

        form=UserRegistrationForm()
    context={'form': form}

    return render(request, 'dashboard/register.html', context)


@login_required(login_url='login')  # Specify the login URL
def profile(request):
    # Assuming the username and password are stored in the User model
    username = request.user.username
    email = request.user.email
    password = request.user.password

    # Create a context dictionary with the data to be passed to the template
    context = {
        'username': username,
        'email': email,
        'password': password,
    }

    # Render the template with the context data
    return render(request, 'dashboard/profile.html', context)




