from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm,MyUserCreationForm
from django.db.models import Q
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.utils.http import base36_to_int, int_to_base36, urlencode
#https://docs.djangoproject.com/en/4.0/ref/contrib/messages/




# rooms = [
#     {'id':1, 'name':'Lets learn Python'},
#     {'id':2, 'name':'Lets learn Java'},
#     {'id':3, 'name':'Lets learn CPP'},
# ]






# Create your views here.



def loginPage(request):  #dont use Login as it is a built in func, will cause a conflict
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        email =request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist.')
        
        user= authenticate(request,email=email,password=password) 

        if user is not None:
            login(request,user)
            return redirect('home')
        
        else:
            messages.error(request, 'Username and Password do not match.')
    context={'page':page}
    return render(request,'base/login_register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page='register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user) #log in the registered user
            return redirect('home')
        else:
            messages.error(request,'an error occurred during registration')
    context={'page':page, 'form':form}
    return render(request,'base/login_register.html',context)


def home(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else  ''

    if(q==''):
         rooms = Room.objects.all()
         room_messages = Message.objects.all()
    else:
        rooms = Room.objects.filter(topic__name=q)#icontains-->case insensitive + can search from initials
        room_messages = Message.objects.filter(Q(room__topic__name=q))
    topics=Topic.objects.all()[0:5]  #only 5 topics
    room_count=rooms.count()
    context={'rooms':rooms, 'topics':topics, 'room_count':room_count,'room_messages':room_messages}


    return render(request,'base/home.html',context)




def room(request,pk):

    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create( 
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )

        room.participants.add(request.user)
        return redirect('room',pk=room.id)

    context={'room':room, 'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)



@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)  #gets the value or creates a new value
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        
        return redirect('home')
    context={'form':form , 'topics':topics}
    return render(request,'base/room_form.html',context)



@login_required(login_url = 'login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    top = Topic.objects.get(name = room.topic)

    if request.user!=room.host:
        return  HttpResponse('You are not allowed here!')


    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name) 
        form = RoomForm(request.POST, instance = room) #data in request.POST will replace the current data in room
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        rooms = Room.objects.filter(topic__name=top)
        if(rooms.count()==0):
            top.delete()
        return redirect('home')
    
    
    context = {'form':form , 'topics':topics,'room':room}
    return render(request, 'base/room_form.html',context)
    

@login_required(login_url = 'login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    topic = Topic.objects.get(name = room.topic)


    if request.user!=room.host:
        return  HttpResponse('You are not allowed here!')

    # for i in Topic.objects.all():
    #     r=Room.objects.filter(topic__name=i)
    #     if(r.count()==0):
    #         i.delete()

    if(request.method=="POST"):

        room.delete()
        rooms = Room.objects.filter(topic__name=topic)
        if(rooms.count()==0):
            topic.delete()



        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})



    
@login_required(login_url = 'login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)


    if request.user!=message.user:
        return  HttpResponse('You are not allowed here!')


    if(request.method=="POST"):
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})



def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user , 'rooms':rooms, 'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)


@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        form.save()
        return redirect('user-profile',pk=user.id)


    context = {'form':form}

    



    return render(request,'base/update-user.html',context)


def topicsPage(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics':topics}
    return render(request,'base/topics.html',context)

def activityPage(request):
    room_messages = Message.objects.all()
    cont = {'room_messages':room_messages}
    return render(request,'base/activity.html',cont)