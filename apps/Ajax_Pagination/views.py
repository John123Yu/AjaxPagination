from django.shortcuts import render, HttpResponse, redirect
from models import Users
from django.core.urlresolvers import reverse
from django.views.generic.edit import View
import json
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.db.models import Q
import math
from datetime import datetime
from pytz import timezone
import pytz
utc = pytz.utc
utc.zone
'UTC'
eastern = timezone('US/Eastern')
totalUsers = {}
usersCount = {}

def index(request):
	global searchName, totalUsers, usersCount
	totalUsers = Users.objects.all()
	usersCount = (totalUsers.count() / 8) + (totalUsers.count() % 8 > 0)
	context = {
		'users': Users.objects.all()[:8],
		'usersCount': usersCount * "x"
	}
	return render(request, 'AjaxPagination/index.html', context)

def new(request):
	context = {
		'users': Users.objects.all()
	}
	return render(request, 'AjaxPagination/new.html', context)

def addUser(request):
	Users.objects.create(firstName = request.POST['firstName'], lastName = request.POST['lastName'], email = request.POST['email'])
	return redirect(reverse('AjaxPagination:new'))

userStart = {}
userEnd = {}
class ChangePage(View):
	def get(self, request):
		context = {
			'users': totalUsers[userStart: userEnd],
			'usersCount': usersCount * "x"
		}
		return render(request, 'AjaxPagination/changePageAjax.html', context)
	def post(self, request):
		global userStart, userEnd, usersCount
		userStart = int(request.POST['pageNumber']) * 8
		userEnd = int(request.POST['pageNumber']) * 8 + 8
		usersCount = (totalUsers.count() / 8) + (totalUsers.count() % 8 > 0)
		return redirect(reverse('AjaxPagination:changePage'))

searchName = {}
class SearchName(View):
	def get(self, request):
		context = {
			'users': searchName,
			'usersCount': usersCount * "x"
		}
		return render(request, 'AjaxPagination/changePageAjax.html', context)
	def post(self, request):
		global searchName, totalUsers, usersCount
		totalUsers = Users.objects.filter( Q(firstName__icontains= request.POST['name']) | Q(lastName__icontains = request.POST['name']) )
		searchName = totalUsers[:8]
		usersCount = (totalUsers.count() / 8) + (totalUsers.count() % 8 > 0)
		return redirect(reverse('AjaxPagination:searchName'))

class StartDate(View):
	def get(self, request):
		context = {
			'users': searchName,
			'usersCount': usersCount * 'x'
		}
		return render(request, 'AjaxPagination/changePageAjax.html', context)
	def post(self, request):
		global searchName, totalUsers, usersCount
		start = eastern.localize( datetime.strptime(request.POST['startDate'], '%Y-%m-%d')  )
		end = eastern.localize( datetime.strptime(request.POST['endDate'], '%Y-%m-%d') )
		totalUsers = Users.objects.filter(created_at__gte=start, created_at__lte=end)
		searchName = totalUsers[:10]
		usersCount = (totalUsers.count() / 8) + (totalUsers.count() % 8 > 0)
		return redirect(reverse('AjaxPagination:searchName'))
