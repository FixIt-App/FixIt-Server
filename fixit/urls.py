"""fixit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from rest_framework.authtoken import views as rest_views

from worktype.views import WorkTypeList, CategoryList

from customer.views import CustomerDetail, CustomerList, AddressList, AddressDetail, confirm_email
from customer.views import get_customer_authenticated, get_customer_adresses
from image.views import  ImageUploadView

from work.views import create_work, get_my_works, WorkDetail

# VERY IMPORTANT, development ONLY, GUNICORN should not go upfront in production, NGINX should
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# end very important




router = routers.DefaultRouter()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api/customers/(?P<pk>[0-9]+)/$', CustomerDetail.as_view(), name='customer-detail'),
    url(r'^api/customers/$', CustomerList.as_view()),
    url(r'^api/customer/authenticated/$', get_customer_authenticated),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/token-auth/', rest_views.obtain_auth_token),
    url(r'^api/myadresses/$', get_customer_adresses),
    url(r'^api/addresses/(?P<pk>[0-9]+)/$', AddressDetail.as_view()),
    url(r'^api/addresses/$', AddressList.as_view()),
    url(r'^api/categories/$', CategoryList.as_view()),
    url(r'^api/worktypes/$', WorkTypeList.as_view()),
    url(r'^api/work/upload-image/$', ImageUploadView.as_view()),
    url(r'^api/myworks/$', get_my_works),
    url(r'^api/work/$', create_work),
    url(r'^api/work/(?P<pk>[0-9]+)/$', WorkDetail.as_view()),
    url(r'^confirmations/(?P<string>[\w\-]+)/$', confirm_email),
    
    
]

# VERY IMPORTANT, development ONLY, GUNICORN should not go upfront in production, NGINX should
urlpatterns += staticfiles_urlpatterns()
# end very important
