from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import re
import bcrypt


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
def index(request):
	return render(request,"belt_django_app/main.html")


def register(request):
	result = User.objects.register(request)
	if result == True:
		return redirect ('/')
	if result == False:
		return redirect ('/friends')

def friends(request):

	if request.session['name'] == "":
		return redirect('/')
	else:
		user_id = request.session['user_id']
		users = User.objects.all().exclude(id=user_id)
		user_list = User.objects.filter(id=user_id)

		userstoshow = user_list[0]
		# this is showing all the friends i have
		otherusers_list = userstoshow.friends.all()
		# now i want to make 2 lists and have them compare to each other to see if my friends are in users then dont add them
		alluserslist= User.objects.all()
		# add all users in the users list
		print 'this is alluserslist'
		print alluserslist
		# now do a check to see if allusers has friends
		random = user_list[0]
		allmyfriends = random.friends.all()
		print 'this is allmyfriends'
		print allmyfriends

		notmyfriends =[]

		for user in alluserslist:
			if user not in allmyfriends:
				notmyfriends.append(user)
		print 'this is notmyfriends'
		print notmyfriends

		if user_list:
			context = {
			'users': users,
			'user': user_list[0],
			'alluserslist':alluserslist,
			'notmyfriends' : notmyfriends
			}
			return render(request,"belt_django_app/friends.html", context)

		else:
			users = User.objects.all()
			context = {
			'users':users,
			}
			return render(request,"belt_django_app/friends.html", context)


def showuser(request, id):
	id = id
	results = User.objects.filter(id=id)
	context= {
	"results" : results[0]
	}
	return render(request,"belt_django_app/showuser.html", context)

def addusertofriend(request, id):
	user_id = request.session['user_id']
	friend_id = id
	dataObject = {
	"user_id" : user_id,
	"friend_id" : friend_id
	}
	results = User.objects.addusertofriend(dataObject)
	if results:
		return redirect ('/friends')

def deletefriend(request, id):
	friend_user_id= id
	user_id= request.session['user_id']
	dataObject={
	'friend_user_id': friend_user_id,
	'user_id': user_id
	}
	results = User.objects.deletefriend(dataObject)
	if results:
		return redirect ('/friends')
	else:
		return redirect ('/friends')

def logout(request):
	request.session['name'] = ""
	request.session['user_id'] = 0
	return redirect('/')

def login(request):
	result = User.objects.login(request)
	if result == True:
		return redirect ('/')
	if result == False:
		return redirect ('/friends')
