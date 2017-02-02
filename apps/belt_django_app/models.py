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
			ps_hashed = user.password
			ps_hashed = ps_hashed.encode()
			if bcrypt.hashpw(password, ps_hashed) == ps_hashed:
				request.session['user_id'] = user.id
				request.session['name'] = user.name
				return x
			else:
				messages.error(request, "email or password does not match")
				x = True
				return x
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

	def addusertofriend(self, dataObject):
		user_id = dataObject['user_id']
		friend_id = dataObject['friend_id']
		newfriendship_list = User.objects.filter(id=dataObject['user_id'])

		newfriendshipperson_list = User.objects.filter(id=dataObject['friend_id'])

		newfriendperson=newfriendshipperson_list[0]
		newfriend=newfriendship_list[0]

		newfriend.friends.add(newfriendperson)

		print 'if it got till here it add the friend'
		return True

	def deletefriend(self, dataObject):

		user_list=User.objects.filter(id=dataObject['friend_user_id'])
		user2_list=User.objects.filter(id=dataObject['user_id'])

		user = user_list[0]
		user2 = user2_list[0]

		test = user.friends.all()
		user.friends.remove(user2)

		print "got to delete function"
		return True
class User(models.Model):

	name = models.CharField(max_length=45)
	last = models.CharField(max_length=45)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	friends = models.ManyToManyField("self",blank=True)
	objects = UserManager()
