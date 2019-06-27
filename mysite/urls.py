"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth import views as admin_views
from myMsgApp import views as my_views
from mysite.core import views as core_views

app_name  = "myMsgApp";

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', core_views.signup, name='signup'),
    #url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^$', my_views.home, name = 'home'),
    url(r'^login/$', admin_views.LoginView.as_view(template_name="registration/login.html"), 
        name = 'mymsgsite_login'), 
    url(r'^mainhome/$', my_views.mainhome, name = 'mainhome'),
    url(r'^mycatprocedures/$', my_views.mycatprocedures, name = 'mycatprocedures'),
    url(r'^resourcecalculation/$', my_views.resourcecalculation, name = 'resourcecalculation'),
    url(r'^developmentpage/$', my_views.developmentpage, name = 'developmentpage'),
    url(r'^reportedhours/$', my_views.reportedhours, name = 'reportedhours'),
    url(r'^capacitynorms/$', my_views.capacitynorms, name = 'capacitynorms'),
    url(r'^codeofconduct/$', my_views.codeofconduct, name = 'codeofconduct'),
    url(r'^competencetracker/$', my_views.competencetracker, name = 'competencetracker'),
    url(r'^technicalreferentsurvey/$', my_views.technicalreferentsurvey, name = 'technicalreferentsurvey'),
    url(r'^traitmentoal/$', my_views.traitmentoal, name = 'traitmentoal'),
    url(r'^whatever/$', my_views.my_view_name, name = 'my_view_name'),
]