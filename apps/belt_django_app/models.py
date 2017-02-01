from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from django.http import HttpResponse
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
class UserManager(models.Manager):
	def login(self, request):
		email = request.POST['email']
		password = request.POST['password']
		print email
		print password
		x = False;

		if len(email) == 0:
			messages.error(request, "email is required")
			x = True;

		elif not User.objects.filter(email = email).exists():
			messages.error(request, "email is not in the database")
			x=True;

		if x:
			return x
		else:
			x = False
			password = password.encode()
			user_list = User.objects.filter(email = email)
			user = user_list[0]
			print user
			print user.name
			print user.password
			print user.id
			ps_hashed = user.password
			ps_hashed = ps_hashed.encode()
			print request.session['name']
			if bcrypt.hashpw(password, ps_hashed) == ps_hashed:
				request.session['user_id'] = user.id
				request.session['name'] = user.name
				print request.session['name']
				print x
				return x
			else:
				messages.error(request, "email or password does not match")
				x = True
				return x

	def register(self, request):
		if request.method == 'POST':
			x = False
			if not EMAIL_REGEX.match(request.POST['email']):
				messages.info(request, ' Invalid email ')
				x = True
			if not NAME_REGEX.match(request.POST['name']):
				messages.info(request, ' Invalid name ')
				x = True
			if not NAME_REGEX.match(request.POST['last']):
				messages.info(request, ' Invalid last ')
				x = True
			if len(request.POST['password']) < 8:
				messages.info(request,'Password must be atleast 8 characters long')
				x = True
			elif request.POST['password'] != request.POST['confirm_password']:
				messages.info(request,'Password and confirm password are not matched')
				x = True
			if x:
				return x

			else:
				password = request.POST['password'].encode()
				hashed = bcrypt.hashpw(password, bcrypt.gensalt())
				already_user_list= User.objects.filter(email=request.POST['email'])
				print request.POST['email']
				print already_user_list
				if not already_user_list:
					print "this means new user"
					user = User.objects.create(name=request.POST['name'],last=request.POST['last'],email = request.POST['email'],password=hashed,)
					print ('**************')
					x = False
					try:
						request.session['name'] = request.POST['name']
						request.session['user_id'] = user.id
					except:
						request.session['name'] = ""
						request.session['user_id'] = 0
					return x

				else:
					print 'this means its a returning user but logging in the wrong place'
					messages.info(request, 'Please login below. Your email already exists in our DB')
					x = True
					return x

class dataManager(models.Manager):
	def addusertofriend(self, dataObject):
		user_id = dataObject['user_id']
		friend_id = dataObject['friend_id']
		Friend.objects.create(user_id=user_id, id=friend_id)
# I AM SUPER STUCK AND FUSTRATED  I KNOW THE REST OF THE THING BUT ITS JSUT THIS ONE THING!!
		print 'till here'
		return True

	def deletefriend(self, dataObject):

		x = Friend.objects.get(user=dataObject['friend_user_id'], user_id=dataObject['user_id'])
		print x

		print "got to delete function"
		return True

class User(models.Model):

	name = models.CharField(max_length=45)
	last = models.CharField(max_length=45)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class Friend(models.Model):
	user = models.ForeignKey(User, default=None)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = dataManager()
