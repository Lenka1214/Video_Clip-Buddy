
# Create your views here.
from django.shortcuts import render, HttpResponse, redirect
# import of models:
from .models import *
from time import gmtime, strftime
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
  # Index route and action Form support Login and Registration page
  # it is called when localhost:8000/index is typed
  # cnt is to be increased by 1 (it is counter)
    if 'user_id' not in request.session:
# assigning to user_id the number of the 1st user - number 1, count=0:       
        request.session['user_id']=1
        request.session['count']=0
    
    request.session['count']=request.session['count']+1

    context = {
        "message": '',
        "time": strftime("%Y-%m-%d %H:%M %p", gmtime()),
        "cnt" : request.session['count'],
    }
    return render(request,"music_app/index.html",context)
def new_user(request):
# NEW USER route: retrieves new user credentials from html and creates this user's record in USER DB'

# retrieving new user infor from FORM, uploading new user in USER table:
    full_name=request.POST['full_name']
    nick_name=request.POST['nick_name']
    email=request.POST['email']
    password=request.POST['password']
    password1=request.POST['password1']

# check of new user credetials:
# checks :  if password and password1 submitted by new user are the same
#           if length of password is too short
#           if user name is too short
#           if email has valid format :
    if password!=password1:
        context = {
                "message": 'your two passwords are not the same, re-enter:',
                "time": strftime("%Y-%m-%d %H:%M %p", gmtime()),
                "cnt" : request.session['count'],
        }
        return render(request,"music_app/index.html",context)
    if len(password)<8:
        context={
                "message": 'your password is less than 8 characters long, re-enter:',
                "time": strftime("%Y-%m-%d %H:%M %p", gmtime()),
                "cnt" : request.session['count'],            
        }
        return render(request,"exam_app/index.html",context)  
    if len(full_name)<3:
        context={
                "message": 'your full name is less than 3 characters long, re-enter:',
                "time": strftime("%Y-%m-%d %H:%M %p", gmtime()),
                "cnt" : request.session['count'],            
        }
        return render(request,"music_app/index.html",context)
    if len(email) < 1:
        context={
                "message": 'email can not be blank, re-enter:',
                "time": strftime("%Y-%m-%d %H:%M %p", gmtime()),
                "cnt" : request.session['count'],          
        }
        return render(request,"music_app/index.html",context)

    if not EMAIL_REGEX.match(email):
        context={
                "message": 'email format is invalid, re-enter:',
                "time": strftime("%Y-%m-%d %H:%M %p", gmtime()),
                "cnt" : request.session['count'],          
        }
        return render(request,"music_app/index.html",context)
  
    User.objects.create(full_name=request.POST['full_name'],
        nick_name=request.POST['nick_name'],
        email=request.POST['email'],password=request.POST['password'])

    return redirect('/index')

def old_user(request):
# retrieve old user email, password
# retrieving of old user which is this_user
# proceed to old user FAVOROTES page (to retrive info from DB and render):

    email=request.POST['email']
    password=request.POST['password']

# retrive existing (named OLD) user from users DB based on given email:
# using FILTER instead of GET to preven ERROR:
    this_user=User.objects.filter(email=email)
    if len(this_user)==0:
        context = {
                "message": 'No user with your email address, re-enter:',
                "time": strftime("%Y-%m-%d %H:%M %p", gmtime()),
                "cnt" : request.session['count'],
        }
        return render(request,"music_app/index.html",context)
# verification of old user password:
    if this_user[0].password!=password:
        context = {
                "message": 'Your password is wrong, re-enter:',
                "time": strftime("%Y-%m-%d %H:%M %p", gmtime()),
                "cnt" : request.session['count'],
        }
        return render(request,"music_app/index.html",context)
# retrive existing (old) user id and update session:
    request.session['user_id']=this_user[0].id
    user_nick=this_user[0].nick_name

# if there no (zero) quotes in the DB, go to creation of the 1st quote, 
# otherwise proceed to the main page which is 'favorites':
    if Quote.objects.count()==0:
        context = {
        'nick_name':user_nick,
        }       
        return render(request, "music_app/from_zero.html",context)  
    

    return redirect('/quotes')

def quotes(request):
# preparation of context for rendering of the MAIN (all quotes) page:#
    this_user=User.objects.get(id=request.session['user_id'])
    quote_favors=Quote.objects.filter(users_likers=this_user)
    quote_others=Quote.objects.exclude(users_likers=this_user)

    context = {
    'nick_name':this_user.nick_name,
    'favorites':quote_favors,
    'all_others':quote_others,
    
    }

    # pass control to favorites.html which render the main page and allow current user
    # to move usual quotes to favorites or to move favorite quotes back to usual (other):
    return render(request,"music_app/favorites.html",context)

    # from_zero: retrieving the 1st quote text and author and uploading it to QUOTE DB to create the 1st record
    # after that go back to the log in route (user should re-enter):
def from_zero(request):
    this_user=request.session['user_id']
    Quote.objects.create(quoted_by=request.POST['quoted_by'],text=request.POST['text'],created_by=User.objects.get(id=this_user))
    this_quote=Quote.objects.get(id=1)
    quote_others=Quote.objects.exclude(users_likers=User.objects.get(id=this_user))

    return redirect('/quotes')



# new quote uploading:
def new_quote(request):

    this_user=request.session['user_id']
    Quote.objects.create(quoted_by=request.POST['quoted_by'],
    text=request.POST['text'], created_by=User.objects.get(id=this_user))
    return redirect ('/quotes')

# current user requested to move specific quote from usual/other quotes to favorites:
def add_favorite(request,id): 
    this_user=User.objects.get(id=request.session['user_id'])
    this_quote=Quote.objects.get(id=id)
    # quote_favors=this_quote.users_likers.add(id=id)
    quote_favors=this_user.favorites.add(this_quote)

    return redirect ('/quotes')

# current user requested to move specic quote from favorites to usual/other quotes:
def remove_favorite(request,id):
    this_user=User.objects.get(id=request.session['user_id'])
    this_quote=Quote.objects.get(id=id)
    # quote_favors=this_quote.users_likers.remove(id=id)
    quote_favors=this_user.favorites.remove(this_quote)
    return redirect ('/quotes')

def user_selected(request,id):
    this_user=User.objects.get(id=id)
    # user_posts=Quote.objects.filter(created_by=id)
    user_posts=Quote.objects.filter(created_by=this_user)
# can i select Favorites like below and pass to html for rendering instead of CREATED_BY?:  
# quote_favors=Quote.users_likers.all(id=id)
    number=len(user_posts)
    context = {
		"user": this_user,
		"user_posts": user_posts,
        "quantity": number,	
    }
    return render(request,"music_app/user.html",context) 


# TOTAL RESET of User and Quote DBs:
def clearance(request):
# other OPTION of how to DELETE whole User and Quote DB in SHELL:
# $ python manage.py sqlflush | python manage.py dbshell
    User.objects.all().delete()
    Quote.objects.all().delete()
    request.session.clear()  
    return redirect('/logout')

def logout(request):
    request.session.clear()
    return redirect('/index')

# Prepares TOTAL RESET of User and Quote DBs, think 7 times before activation!:
# ALL existing User and Quote data will be DELETED and after that u should start from ZERO
# (reset.html still TBD. Should loop through id of User and Quote and DELETE each record)
# def total_reset(request):

#     user_number=User.objects.count()
#     quote_number=Quote.objects.count()
#     context={
#         "user_num":user_number,
#         "quote_num":quote_number,
#     }
#     return render(request,"exam_app/reset.html",context)