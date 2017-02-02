from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

#=====================================
# 				Render
#=====================================
def index(request):
	return render(request,"belt_django_app/main.html")

def friends(request):
	if 'user_id' in request.session:

		user_id = request.session['user_id']
		users = User.objects.exclude(id = user_id)
		user_list = User.objects.filter(id = user_id)

		usertoshow = user_list[0]

		friend_ids = usertoshow.friends.values_list('id', flat=True)
		notmyfriends = User.objects.exclude(id__in=friend_ids).exclude(id=user_id)

		context = {
			'user': usertoshow,
			'notmyfriends' : notmyfriends
		}
		return render(request,"belt_django_app/friends.html", context)

	return redirect('/')

def showuser(request, id):
	results = User.objects.filter(id = id)
	if results:
		context = {
			"results" : results[0]
		}
		return render(request,"belt_django_app/showuser.html", context)
	return redirect('/friends')

#=====================================
# 			Process
#=====================================

def addusertofriend(request, id):
	user_id = request.session['user_id']
	User.objects.addusertofriend(user_id, id)
	return redirect ('/friends')

def deletefriend(request, id):
	user_id = request.session['user_id']
	User.objects.deletefriend(user_id, id)
	return redirect ('/friends')

#=====================================
# 			login reg
#=====================================

def login(request):
	if request.method == 'POST':
		result = User.objects.login(request.POST)
		if result['status']:
			request.session['user_id'] = result['user_id']
			request.session['name'] = result['user_name']
			return redirect ('/friends')
		else:
			for errorStr in result['errors']:
				messages.error(request, errorStr)
	return redirect ('/')

def register(request):
	if request.method == 'POST':
		result = User.objects.register(request.POST)
		if result['status']:
			request.session['user_id'] = result['user_id']
			request.session['name'] = result['user_name']
			return redirect ('/friends')
		else:
			for errorStr in result['errors']:
				messages.error(request, errorStr)
	return redirect ('/')

def logout(request):
	request.session.clear()
	return redirect('/')
