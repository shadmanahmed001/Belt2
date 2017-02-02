from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
	def login(self, post):
		email = post['email'].lower().strip()
		password = post['password']

		errors =[]
		if len(email) == 0:
			errors.append('email is required')
		elif not User.objects.filter(email = email).exists():
			errors.append('email is not in the database')

		if not errors:
			user_list = User.objects.filter(email = email)
			user = user_list[0]
			password = password.encode()
			ps_hashed = user.password.encode()
			if bcrypt.hashpw(password, ps_hashed) == ps_hashed:
				return {'status': True, 'user_id': user.id, 'user_name' : user.name}
			else:
				errors.append('email or password does not match')
		return {'status': False, 'errors': errors}

	def register(self, post):
		email = post['email'].lower().strip()
		name = post['name']
		last = post['last']
		password = post['password']
		confirm_password = post['confirm_password']

		errors = []
		if not EMAIL_REGEX.match(email):
			errors.append(' Invalid email ')
		if not NAME_REGEX.match(name):
			errors.append(' Invalid name ')
		if not NAME_REGEX.match(last):
			errors.append(' Invalid last ')
		if len(password) < 8:
			errors.append(' Password must be atleast 8 characters long ')
		elif password != confirm_password:
			errors.append(' Password and confirm password are not matched ')

		if not errors:
			already_user_list = User.objects.filter(email=email)
			if not already_user_list:
				password = password.encode()
				hashed = bcrypt.hashpw(password, bcrypt.gensalt())
				print "this means new user"
				user = User.objects.create(name=name,last=last,email = email,password=hashed,)
				print ('**************')
				return {'status': True, 'user_id': user.id}
			else:
				errors.append('Please login below. Your email already exists in our DB')
				print 'this means its a returning user but logging in the wrong place'

		return {'status': False, 'errors': errors}

	def addusertofriend(self, user_id, friend_id):
		user_list = User.objects.filter(id = user_id)
		friend_list = User.objects.filter(id = friend_id)
		if friend_list:
			friend = friend_list[0]
			me = user_list[0]
			me.friends.add(friend)
		return True

	def deletefriend(self, myId, friendId):
		user_list = User.objects.filter(id = friendId)
		user2_list = User.objects.filter(id = myId)
		if user_list:
			friend = user_list[0]
			me = user2_list[0]
			me.friends.remove(friend)
		return True

class User(models.Model):
	name = models.CharField(max_length=45)
	last = models.CharField(max_length=45)
	email = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	friends = models.ManyToManyField("self", blank=True)
	objects = UserManager()
