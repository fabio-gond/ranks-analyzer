from django.shortcuts import render
from django.shortcuts import redirect

#-------------------- PAGES -------------------

def index(request):
    if not request.user.is_authenticated:
         return redirect('account_login')

    template = 'index.html'
    context = {}
    return render(request, template, context)