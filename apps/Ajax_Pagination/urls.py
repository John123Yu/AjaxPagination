from django.conf.urls import url, include 
from . import views
from views import ChangePage, SearchName, StartDate

urlpatterns = [
	url(r'^$', views.index, name = "index"),
	url(r'^new$', views.new, name = "new"),
	url(r'^addUser$', views.addUser, name = "addUser"),
	url(r'^changePage$', ChangePage.as_view(), name = "changePage"),
	url(r'^searchName$', SearchName.as_view(), name = "searchName"),
	url(r'^startDate$', StartDate.as_view(), name = "startDate")

	]