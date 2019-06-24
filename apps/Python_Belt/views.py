from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# Create your views here.
def index(request):
    return render(request,"index.html")

def register(request):
    error=False
    #print(request.POST)
    if len(request.POST['first_name'])<1:
        messages.error(request,"Please enter a first name!", extra_tags='first')
        error= True
    if len(request.POST['last_name'])<1:
        messages.error(request,"Please enter a last name!", extra_tags='last')
        error = True
    if not EMAIL_REGEX.match(request.POST['email']):    # test whether a field matches the pattern
        messages.error(request, "Invalid Email!", extra_tags='invalidemail')
        error = True
    if len(request.POST['password'])<2:
        messages.error(request,"Please enter a better password!", extra_tags='password')
        error = True
    if request.POST['password'] != request.POST['confirm']:
        messages.error(request,"Passwords do not match!" , extra_tags='confirm')
        error = True
    if not any(x.isupper() for x in request.POST['password']):
        messages.error(request,"Password needs upper case!" , extra_tags='upper')
        error = True
    if not any(x.isdigit() for x in request.POST['password']):
        messages.error(request,"Passwords need a digit!" , extra_tags='digit')
        error = True

    matching_users = User.objects.filter(email=request.POST['email'])
    if len(matching_users) > 0:
        messages.error(request, "Sorry, email already taken", extra_tags='email')
        error = True

    if error:
        return redirect('/')
    
    hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

    user = User.objects.create(first_name=request.POST['first_name'], last_name= request.POST['last_name'], email=request.POST['email'], password = hashed)
    
    request.session['user_id'] = user.id
    print(user)
    print(request.session['user_id'])
    return redirect('/')

def login(request):
    print(request.POST)
    matching_users = User.objects.filter(email=request.POST['log_email'])
    if len(matching_users) > 0:
        #email matched now check pw
        user = matching_users[0]
        if bcrypt.checkpw(request.POST['log_password'].encode() , user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/main')
        else:
            messages.error(request,"Invalid Credentials!")   
    else:
        messages.error(request,"Invalid Credentials!")  
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def main(request):
    if not 'user_id' in request.session:
        return redirect('/')
    else:
        if request.method == "GET" :
            context = {
                "quotes" : Quote.objects.all(),
                "users" : User.objects.filter(id = request.session['user_id']),
            }
            print(request.session['user_id'])
            return render(request,'main.html', context)
        if request.method == "POST":
            error=False
            #print(request.POST)
            if len(request.POST['author'])<4:
                messages.error(request,"Author name must be more than 3 characters!", extra_tags='authlen')
                error= True
            if len(request.POST['quote'])<11:
                messages.error(request,"Quote  must be more than 10 characters!", extra_tags='quotelen')
                error = True
            if error:
                return redirect('/main')

            user = User.objects.get(id=request.session['user_id'])
            quote = Quote.objects.create(author = request.POST['author'] , quote = request.POST['quote'])
            user.quotes.add(quote)
            return redirect('/main')

def edit(request):
    if not 'user_id' in request.session:
        return redirect('/')
    else:  
        if request.method == "GET" :
            context = {
                "users" : User.objects.filter(id = request.session['user_id']),
            }
            return render(request,"editform.html",context)
        if request.method == "POST":
            matching_users = User.objects.filter(email=request.POST['email'])
            error=False
            #print(request.POST)
            if len(request.POST['first_name'])<1:
                messages.error(request,"Please enter a first name!", extra_tags='first')
                error= True
            if len(request.POST['last_name'])<1:
                messages.error(request,"Please enter a last name!", extra_tags='last')
                error = True
            if not EMAIL_REGEX.match(request.POST['email']):    # test whether a field matches the pattern
                messages.error(request, "Invalid Email!", extra_tags='invalidemail')
                error = True
            if len(matching_users) > 0:
                messages.error(request, "Sorry, email already taken", extra_tags='email')
                error = True

        if error:
            return redirect('/edit')

    user = User.objects.get(id=request.session['user_id'])
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.save()
    return redirect(f"/users/{user.id}")
            
def like(request, qID):
    if not 'user_id' in request.session:
        return redirect('/')
    else:
        quote = Quote.objects.get(id=qID)
        like = Like.objects.create(liked=True)
        quote.likes.add(like)
        quote.likecount += 1
        quote.likedby = request.session['user_id']
        quote.save()
        return redirect('/main')

def delete(request, qID):
    if not 'user_id' in request.session:
        return redirect('/')
    else:  
        quote = Quote.objects.get(id=qID)
        quote.delete()
        return redirect('/main')

def showuser(request, uID):
    if not 'user_id' in request.session:
        return redirect('/')
    else: 
        context = {
            "quotes" : Quote.objects.all(),
            "users" : User.objects.filter(id = uID),
        }
        return render(request,'showuser.html', context)