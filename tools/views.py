from django.shortcuts import render
from .models import Log

# -------------------- PAGES -------------------


def index(request):
    template = 'tools/index.html'

    context = {
        "action": None,
    }

    return render(request, template, context)

def system_logs(request):
    logs = Log.objects.all().order_by('-time')[:1000]

    template = 'tools/log_viewer.html'
    context = {
        "logs": logs
    }
    return render(request, template, context)