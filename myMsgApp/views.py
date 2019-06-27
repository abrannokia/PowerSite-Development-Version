from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
from subprocess import Popen, PIPE, STDOUT
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import os
from django.contrib import messages
from Calculations import FTECaclulation, ReportedHours, WeeklyUtilisation
from TableCreators import *
from SQLtoCSV import SQLtoCSV
import datetime


def home(request):
    return render(request, "myMsgApp/home.html",
                  {',pText': 'Please click the login button below to begin:',
                   'h1Text': 'Welcome to NOKIA Timisoara NI GSD official web page'
                   })
# Create your views here.
@login_required
def mycatprocedures(request):
    return render(request, "myMsgApp/mycatprocedures.html",
                  {'h1Text': 'Site Versions',
                   'pText': 'test'
                   })
@login_required
def capacitynorms(request):
    return render(request, "myMsgApp/capacitynorms.html",
                  {'h1Text': 'Site Versions',
                   'pText': 'test'
                   })

@login_required
def main(request):
    #if not request.user.is_authenticated():
    return render(request, "main2.html",
                      {'pText': 'Welcome to the NOKIA Timisoara NI GSD official web page! You are loged in!'
                   })
@login_required
def mainhome(request):
    return render(request, "myMsgApp/mainhome.html")

def codeofconduct(request):
    return render(request, "myMsgApp/codeofconduct.html",
                  {'pText': 'You have been successfully logged in!'
                   })
@login_required
def resourcecalculation(request):
    if request.method == 'GET':
            try:
                FTECaclulation()
                WeeklyUtilisation()
                return render(request, 'myMsgApp/resourcecalculation.html')
            except:
                messages.warning(request, 'Error while running calculation scripts. Please contact site administrator!')
                return render(request, 'myMsgApp/resourcecalculation.html')
    elif request.method == 'POST':
            return render(request, 'yourapp/output.html')
@login_required
def developmentpage(request):
    return render(request, "myMsgApp/developmentpage.html",
                 )
@login_required
def my_view_name(request):
    if request.method == 'GET':
        try:
            SQLtoCSV()
            messages.warning(request, str(datetime.datetime.now()) + ' - Please be informed that the operations have been performed successfully!')
            return render(request, "myMsgApp/developmentpage.html")
        except:
                messages.warning(request, 'Error while running calculation scripts. Please contact site administrator!')
                return render(request, "myMsgApp/developmentpage.html")
@login_required
def reportedhours(request):
    if request.method == 'GET':
            try:
                ReportedHours()
                return render(request, 'myMsgApp/reportedhours.html')
            except:
                messages.warning(request, 'Error while running calculation scripts. Please contact site administrator!')
                return render(request, 'myMsgApp/reportedhours.html')
    elif request.method == 'POST':
            return render(request, 'yourapp/output.html')

@login_required
def competencetracker(request):
    if request.method == 'GET':
        try:
            messages.warning(request, str(datetime.datetime.now()) + ' - Please be informed that the operations have been performed successfully!')
            return render(request, "myMsgApp/competencetracker.html")
        except:
                messages.warning(request, 'Error while running calculation scripts. Please contact site administrator!')
                return render(request, "myMsgApp/competencetracker.html")
@login_required
def traitmentoal(request):
    return render(request, "myMsgApp/traitmentoal.html",
                  {'pText': 'You have been successfully logged in!'
                   })

@login_required
def technicalreferentsurvey(request):
    if request.method == 'GET':
        try:
            messages.warning(request, str(datetime.datetime.now()) + ' - Please be informed that the operations have been performed successfully!')
            return render(request, "myMsgApp/technicalreferentsurvey.html")
        except:
                messages.warning(request, 'Error while running calculation scripts. Please contact site administrator!')
                return render(request, "myMsgApp/technicalreferentsurvey.html")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.userprofile .email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')
