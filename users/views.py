from django.shortcuts import render
from django.http import JsonResponse
from allauth.account.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import CustomUser
from allauth.account.models import EmailAddress
from .forms import AccountInfoForm

#------------------------------  API ------------------------------------

def checkUserPass(request, password):
     return JsonResponse({"result" : request.user.check_password(password)},)

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
     success_url = reverse_lazy('account')

def account(request):
     user = request.user
     if not request.user.is_authenticated:
          return redirect('account_login')    

     template = 'account/account.html'
     action = request.POST.get('action', None)
     accountInfoForm = AccountInfoForm(instance = user)
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


