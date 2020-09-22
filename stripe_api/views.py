from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings # new
import stripe
from django.urls import reverse
from users.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from tools.utils import log
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from .models import Plan, OneTimeProduct

@csrf_exempt
def config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_TEST_PUBLIC_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request, mode, stripePriceId):
    ctx = 'STRIPE API - create_checkout_session'
    if request.method == 'GET':
        domain_url = 'http://127.0.0.1:8000'
        stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - lets capture the payment later
            # [customer_email] - lets you prefill the email input in the form
            # For full details see https:#stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + reverse('users:subscriptions') + '/activated?stripe_session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + reverse('users:subscriptions'),
                payment_method_types=['card'],
                mode=mode, #payment o subscription o setup
                customer = request.user.stripe_cust_id,
                line_items=[
                    {
                        'price': stripePriceId,
                        'quantity': 1
                    }
                ]
            )

            request.user.plan_current_checkout = None
            request.user.one_time_current_checkout = None

            if mode == 'subscription':
                try: 
                    plan = Plan.objects.get(price_id = stripePriceId)
                    request.user.plan_current_checkout = plan
                except ObjectDoesNotExist as e:
                    log("Plan not found with price_id = " + str(stripePriceId),request.user,ctx,2)
                    return JsonResponse({'error': "Plan not found with price_id = " + str(stripePriceId)})
            else:
                try: 
                    prod = OneTimeProduct.objects.get(price_id = stripePriceId)
                    request.user.one_time_current_checkout = prod
                except ObjectDoesNotExist as e:
                    log("One Time Product not found with price_id = " + str(stripePriceId),request.user,ctx,2)
                    return JsonResponse({'error': "One Time Product not found with price_id = " + str(stripePriceId)})
            
            request.user.stripe_checkout_session_id = checkout_session['id']
            request.user.save()
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

@csrf_exempt
def webhook(request):
    ctx ="STRIPE WEBHOOK"
    payload = request.body

    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None


    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.DJSTRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        log("Invalid Payload", None, ctx, 2)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        log("Invalid signature", None, ctx, 2)
        return HttpResponse(status=400)
    
    data = event['data']['object']
    print(event['type'])
    # Lo utilizzo per i piani non ricorsivi
    if event['type'] == 'checkout.session.completed':
        print("ok checkout.session.completed")
        stripe_cust_id = data['customer']

        try:
            customer = CustomUser.objects.get(stripe_cust_id = stripe_cust_id)
        except ObjectDoesNotExist as e:
            log("Event " + event['type'] + ": Customer not found with stripe_cust_id = " + str(stripe_cust_id),None,ctx,2)
            return HttpResponse(status=200)
        
        print(data)
        if customer.plan_current_checkout != None and customer.stripe_checkout_session_id == data['id']:
            customer.plan = customer.plan_current_checkout
            if customer.plan_current_checkout.interval == 'month':
                customer.plan_paid_until = date.today() + relativedelta(months=1)
            customer.save()
            log("Event " + event['type'] + ": Subscription updated for customer " + customer.email, None, ctx, 0)
        if customer.one_time_current_checkout != None and customer.stripe_checkout_session_id == data['id']:
            customer.one_time_product = customer.one_time_current_checkout
            if customer.one_time_current_checkout.interval == 'month':
                customer.one_time_paid_until = date.today() + relativedelta(months=1)
            customer.save()
            log("Event " + event['type'] + ": Subscription updated for customer " + customer.email, None, ctx, 0)
                
    # Lo utilizzo per i piani ricorsivi
    if event['type'] == 'customer.subscription.created' or event['type'] == 'customer.subscription.updated':
        stripe_cust_id = data['customer']
        try:
            customer = CustomUser.objects.get(stripe_cust_id = stripe_cust_id)
        except ObjectDoesNotExist as e:
            log("Event " + event['type'] + ": Customer not found with stripe_cust_id = " + str(stripe_cust_id),None,ctx,2)
            return HttpResponse(status=200)
        
        paid_until = datetime.fromtimestamp(data['current_period_end'])
        status = data['status']

        price_id = data['items']['data'][0]['price']['id']
        prod_id = data['items']['data'][0]['price']['product']
        try:
            plan = Plan.objects.get(price_id = price_id, product_id = prod_id )
        except ObjectDoesNotExist as e:
            log("Event " + event['type'] + ": Plan not found with price_id = " + str(price_id) + " and prod_id = " + str(prod_id),None,ctx,2)
            return HttpResponse(status=200)

        if status == 'active':
            customer.plan = plan
            customer.paid_until = paid_until
            customer.save()
            log("Event " + event['type'] + ": Subscription updated for customer " + customer.email, None, ctx, 0)



    # Fulfill the purchase...
    #handle_checkout_session(session)

    return HttpResponse(status=200)
