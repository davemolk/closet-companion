from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Message
from django.contrib.auth.models import User
from .forms import MessageForm, CustomUserCreationForm

# Create your views here.

def index(request):
    return render(request, 'index.html')


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('account')
        
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'user/login.html')


def logoutUser(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('index')


def signupUser(request):
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'User account created!')
            login(request, user)
            return redirect('account')
        else:
            messages.error(request, 'An error has occurred during registration')
            return redirect('signup')
    context = {'form': form}
    return render(request, 'user/signup.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    items = profile.item_set.all()

    context = {'profile': profile, 'items': items}
    return render(request, 'user/account.html', context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount,}
    return render(request, 'user/inbox.html', context)


@login_required(login_url="login")
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {'message': message,}
    return render(request, 'user/message.html', context)

@login_required(login_url="login")
def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try: 
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()

            messages.success(request, 'Your message was sent successfully.')
            return redirect('store')

    context = {'recipient': recipient, 'form': form}
    return render(request, 'user/message_form.html', context)

@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message deleted!')
        return redirect('inbox')

    context = {'object': message}
    return render(request, 'delete_template.html', context)