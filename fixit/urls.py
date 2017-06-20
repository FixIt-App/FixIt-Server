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
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers
from rest_framework.authtoken import views as rest_views

from worktype.views import WorkTypeList, CategoryList
from worktype.web import WorkTypeList

from work.web import schedule_work_view

from customer.views import CustomerDetail, CustomerList, AddressList, AddressDetail, confirm_email, confirm_phone, my_confirmation
from customer.views import get_customer_authenticated, get_customer_adresses, resend_sms_code, is_email_available, is_phone_available

from work.views import start_work, calculate_price

from customer.web import login, sign_up, add_address

from image.views import  ImageUploadView

import os

from work.views import create_work, get_my_works, WorkDetail, assign_work, get_total_price, get_ordered_works

from worktype.web import landing

from notification.views import register_device, remove_device_token

router = routers.DefaultRouter()

urlpatterns = [
     url(r'^$', landing, name='landing'),
    url(r'^login/', login, name='login'),
    url(r'^signup/', sign_up, name='signup'),
    url(r'^trabajos/$', WorkTypeList.as_view(), name='works'),
    url(r'^trabajos/(?P<url_name>.*)/agendar-cita/$', schedule_work_view, name='schedule-work'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/customers/(?P<pk>[0-9]+)/$', CustomerDetail.as_view(), name='customer-detail'),
    url(r'^api/customers/$', CustomerList.as_view()),
    url(r'^api/customer/authenticated/$', get_customer_authenticated),
    url(r'^api/customer/email/(?P<email>.*)/available/$', is_email_available),
    url(r'^api/customer/phone/(?P<phone>\+[0-9]+)/available/$', is_phone_available),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/token-auth/', rest_views.obtain_auth_token),
    url(r'^api/myadresses/$', get_customer_adresses),
    url(r'^api/addresses/(?P<pk>[0-9]+)/$', AddressDetail.as_view()),
    url(r'^api/addresses/$', AddressList.as_view()),
    url(r'^agregar/direccion/$', add_address, name='add_address'),
    url(r'^api/categories/$', CategoryList.as_view()),
    url(r'^api/worktypes/$', WorkTypeList.as_view()),
    url(r'^api/work/upload-image/$', ImageUploadView.as_view()),
    url(r'^api/myworks/$', get_my_works),
    url(r'^api/work/ordered/$', get_ordered_works),
    url(r'^api/work/$', create_work),
    url(r'^api/work/(?P<pk>[0-9]+)/price/$', get_total_price),
    url(r'^api/work/(?P<pk>[0-9]+)/worker/$', assign_work),
    url(r'^api/work/(?P<pk>[0-9]+)/$', WorkDetail.as_view()),
    url(r'^api/worker/(?P<worker_id>[0-9]+)/work/(?P<work_id>[0-9]+)/confirmation/$', start_work),
    url(r'^api/myconfirmations/', my_confirmation),
    url(r'^api/phone/confirmations/', confirm_phone),
    url(r'^confirmations/(?P<code>[\w\-]+)/$', confirm_email),
    url(r'^api/devicetoken/$', register_device),
    url(r'^api/dynamicprice/$', calculate_price),
    url(r'^api/devicetoken/(?P<token>.*)/$', remove_device_token),
    url(r'^api/resend-sms-code/$', resend_sms_code),
    url(r'^api/', include(router.urls)),
] 
if settings.DEBUG == True:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.STATIC_ROOT, "public"))
