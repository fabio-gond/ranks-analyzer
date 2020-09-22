from django.shortcuts import render
from django.http import JsonResponse
from allauth.account.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import CustomUser
from allauth.account.models import EmailAddress
from .forms import AccountInfoForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings # new
from stripe_api.models import Plan, OneTimeProduct
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from datetime import date

#------------------------------  API ------------------------------------

def checkUserPass(request, password):
     return JsonResponse({"result" : request.user.check_password(password)},)

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
     success_url = reverse_lazy('account')

@login_required
def account(request):
     user = request.user
     """ 
     if not request.user.is_authenticated:
          return redirect('account_login')  """   

     template = 'account/account.html'
     action = request.POST.get('action', None)
     accountInfoForm = AccountInfoForm(instance = request.user)
     alerts = []

     if action == 'update-account-info':
          accountInfoForm = AccountInfoForm(request.POST,instance = user)
          oldEmail = user.email

          if accountInfoForm.is_valid():
               #email = accountInfoForm.cleaned_data.get("email")

               """ if email != oldEmail and CustomUser.objects.filter(email=email):
                    print("alerta")
                    alerts.append({"type" : "danger", "text": "Email already exists." })
               else:
                    accountInfoForm.save()
                    try:
                         emailObj = EmailAddress.objects.get(user = user)
                         emailObj.email = user.email
                         emailObj.verified = False
                         emailObj.save()
                    except Exception as e:
                         pass
                    alerts.append({"type" : "success", "text": "Profile data succesfully updated" }) """
               
               accountInfoForm.save()
          else:
               print("Form non valid")
               print(accountInfoForm.errors)
               print(accountInfoForm.non_field_errors)


          """ email = request.POST.get('email', None)
          t = CustomUser.objects.filter(email = email)
          if len(t)>0:
               alerts.append({"type" : "danger", "text": "E-mail address already existing" })
          else:
               request.user.first_name = request.POST.get('profile-first-name', None)
               request.user.last_name = request.POST.get('profile-last-name', None)
               request.user.email = request.POST.get('profile-email', None)
               request.user.save()

               try:
                    emailObj = EmailAddress.objects.get(user = request.user)
                    emailObj.email = request.user.email
                    emailObj.verified = False
                    emailObj.save()
               except Exception as e:
                    pass
               
               alerts.append({"type" : "success", "text": "Profile data succesfully updated" }) """
          

     context = {
          "alerts" : alerts,
          "accountInfoForm" : accountInfoForm
     }
     return render(request, template, context)

def accountOLD(request):
     if not request.user.is_authenticated:
          return redirect('account_login')

     template = 'account/account.html'
     action = request.POST.get('action', None)
     alerts = []

     if action == 'update-account-info':
          email = request.POST.get('email', None)
          t = CustomUser.objects.filter(email = email)
          if len(t)>0:
               alerts.append({"type" : "danger", "text": "E-mail address already existing" })
          else:
               request.user.first_name = request.POST.get('profile-first-name', None)
               request.user.last_name = request.POST.get('profile-last-name', None)
               request.user.email = request.POST.get('profile-email', None)
               request.user.save()

               try:
                    emailObj = EmailAddress.objects.get(user = request.user)
                    emailObj.email = request.user.email
                    emailObj.verified = False
                    emailObj.save()
               except Exception as e:
                    pass
               
               alerts.append({"type" : "success", "text": "Profile data succesfully updated" })
          

     context = {
          "alerts" : alerts
     }
     return render(request, template, context)

def subscriptions(request):
     template = 'account/subscriptions.html'

     userPlan = request.user.plan
     userOneTime = request.user.one_time_product

     planPaidUntil = request.user.plan_paid_until
     oneTimePaidUntil = request.user.one_time_paid_until

     stripePlans = Plan.objects.all()
     plans = {}
     for plan in stripePlans:
          plans[plan.code]= plan
     
     stripeOneTime = OneTimeProduct.objects.all()
     oneTimeProds = {}
     for prod in stripeOneTime:
          oneTimeProds[prod.code]= prod

     if oneTimePaidUntil == None or oneTimePaidUntil <= date.today():
          userOneTime = None
     
     context = {
          "plans" : plans,
          "oneTimeProds" : oneTimeProds,
          "userPlan" : userPlan,
          "userOneTime" : userOneTime,
     }
     return render(request, template, context)

def succesfulSubscription(request):
     template = 'account/subscription_success.html'
     
     if request.GET.get("stripe_session_id", None) is not None:
          print("Pagamento ricevuto")
          print(request.GET.get("stripe_session_id", None))

     context = {
         
     }
     return render(request, template, context)

