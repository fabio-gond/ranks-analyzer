from .models import Log
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


to_tz = timezone.get_default_timezone()

# SEVERITY: 0 = message | 1 = warning | 2 = error


def log(text, user, context, severity):
    log = Log(log=text, user = user, context=context,
              time=datetime.now().astimezone(to_tz), 
              severity=severity)
    log.save()
    if severity > 1:
        print("Errore critico!")
        # Mandare email!

