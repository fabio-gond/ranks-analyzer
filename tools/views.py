from django.shortcuts import render
from .models import Log
from .utils import log
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from analyze.models import Product, ProductParent, Keyword, AmazonRank
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from users.models import CustomUser
import json

# -------------------- PAGES -------------------


def index(request):
    template = 'tools/index.html'

    context = {
        "action": None,
    }

    if request.POST.get("action", None) == 'upload-ranks-rankanalyzer':
        response = json.loads(loadScrapedRanks(request).content)
        context = {
                "action": 'upload-ranks-rankanalyzer',
                "success" : response['success'],
                "message" : response['message'],
                "errors": response['errors']
            }
            


    return render(request, template, context)

def system_logs(request):
    logs = Log.objects.all().order_by('-time')[:1000]

    template = 'tools/log_viewer.html'
    context = {
        "logs": logs
    }
    return render(request, template, context)



#-------------------  API ---------------------

@csrf_exempt
def loadScrapedRanks(request):
    ctx = "TOOLS - load_scraped_ranks"
    # Aggiornamento ranking da file IndexReports

    try:
        ranksFile = request.FILES["ranks_file.xlsx"]
    except Exception as e:
        log("Nessun Ranks File", request.user, ctx, 2)
        return JsonResponse({
            'success': False,
            'errors': ['no rank file']
            })

    rankDf = pd.read_excel(ranksFile)

    errors = []
    cntUploads = 0
    # Aggiunge rank a kw_rankings
    for i, row in rankDf.iterrows():
        customerEmail = str(row['customerEmail'])

        try:
            customer = CustomUser.objects.get(email = customerEmail)
        except ObjectDoesNotExist:
            errors.append("Customer not found at row " + str(i))
            continue  

        marketplace = row['marketplace']  
        if marketplace == '' or marketplace=='nan':
            errors.append("No marketplace at row " + str(i))
            continue 


        for asin in str(row['asin']).split("|"):
            try:
                product = Product.objects.get(asin=asin, marketplace= marketplace, user = customer)
            except ObjectDoesNotExist:
                errors.append("Prodotto con ASIN " + asin + " e mp " + marketplace + " non presente nel DB per questo customer")
                continue

            try:
                dbKw = Keyword.objects.get(
                    keyword=row['keyword'],
                    product=product,
                    marketplace=row['marketplace'])
            except ObjectDoesNotExist:
                dbKw = Keyword(
                    keyword=row['keyword'],
                    product=product,
                    marketplace=row['marketplace'])
                dbKw.save()

            try:
                dbRank = AmazonRank.objects.get(
                    keyword=dbKw, product=product, day=row['dVal'])
            except ObjectDoesNotExist:
                dbRank = AmazonRank(
                    keyword=dbKw, product=product, day=row['dVal'])

            topSeller = str(row['topSeller']).strip()
            if topSeller == 'nan': topSeller = ''

            if asin == row['foundAsin']:
                dbRank.amazon_choice = row['amazonChoice']
                dbRank.rank = int(row['rank'])
                dbRank.rank_sponsored = int(row['rankSponsored'])
                dbRank.page = int(row['page'])
                dbRank.pos_in_page = int(row['posInPage'])
                dbRank.pos_in_page_sponsored = int(row['posInPageSponsored'])
                dbRank.top_seller = topSeller
                dbRank.indexed = row['indexed']

            dbRank.save()
            
            cntUploads += 1
    
    message = str(cntUploads) + " keyword ranks succesfully uploaded"

    return JsonResponse({
        "success": True,
        "message": message,
        "errors": errors,
        })