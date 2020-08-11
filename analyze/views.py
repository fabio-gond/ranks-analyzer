from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from .models import Product, ProductParent, Keyword
import pandas as pd
import mimetypes
from django.conf import settings
import csv
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.urls import reverse
from tools.utils import log

#-------------------- PAGES -------------------

def index(request):
    return redirect('analyze:products')

def products(request, reverseView = None):
    ctx = "PRODUCTS"
    #if not request.user.is_authenticated:
    #     return redirect('account_login')

    if request.POST.get("action") == 'upload_products_model':
        result = checkProductsFile(request, True)
        print("DONE")
        print(result)
        
    parents = ProductParent.objects.filter(user = request.user)
    childs = Product.objects.filter(user = request.user)
    
    products = {
        "no_parent": {
            "parent" : None,
            "childs" : []
        }
    }
   
    for parent in parents:
        products[parent.code] = {
            "parent" : parent,
            "childs" : []
        }
    
    for child in childs:
        
        if child.parent is not None:
            parentCode = child.parent.code
            if parentCode in products:
                products[parentCode]["childs"].append(child)
            else:
                products["no_parent"]["childs"].append(child)
        else:
           products["no_parent"]["childs"].append(child) 
    
    table = []
    for code, prod in products.items():
        if code!= "no_parent":
            table.append({
                'mp' : prod['parent'].marketplace,
                'parentCode' : code,
                'childCode' : "",
                'asin' : prod['parent'].asin,
                'keywords': ''
            })

            for child in prod['childs']:
                table.append({
                    'mp' : child.marketplace,
                    'parentCode' : "",
                    'childCode' : child.code,
                    'asin' : child.asin,
                    'keywords': Keyword.objects.filter( product = child, marketplace = child.marketplace ).count()
                })
        else:
            for child in prod['childs']:
                table.append({
                    'mp' : child.marketplace,
                    'parentCode' : "",
                    'childCode' : child.code,
                    'asin' : child.asin,
                    'keywords': Keyword.objects.filter( product = child, marketplace = child.marketplace ).count()
                })


    template = 'products.html'
    context = {
        "table" : table
    }
    return render(request, template, context)

def downloadCurrentProductsModel (request):
    parents = ProductParent.objects.filter(user = request.user)
    variants = Product.objects.filter(user = request.user)

    table = []
    for parent in parents:
        table.append({
            "marketplace": parent.marketplace,
            "seller_sku": parent.code,
            "parent_asin": "",
            "product_asin": parent.asin,
            "type": "parent"
        })

        for variant in variants.filter(parent = parent):
            table.append({
                "marketplace": variant.marketplace,
                "seller_sku": variant.code,
                "parent_asin": parent.asin,
                "product_asin": variant.asin,
                "type": "variant"
            })
    
    for variant in variants.filter(parent = None):
            table.append({
                "marketplace": variant.marketplace,
                "seller_sku": variant.code,
                "parent_asin": "",
                "product_asin": variant.asin,
                "type": "variant"
            }) 
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products_model.csv"'

    writer = csv.writer(response)

    writer.writerow(['', 'max 32 char', '', ''])
    writer.writerow(['marketplace', 'seller_sku', 'parent_asin', 'product_asin','type'])

    for row in table:
        writer.writerow([
            row["marketplace"],
            row["seller_sku"],
            row["parent_asin"],
            row["product_asin"],
            row["type"],
        ])

    return response
#    return JsonResponse(table, safe = False)

def uploadKeywordsFile(request):
    ctx = "UPLOAD KEYWORD FILE"
    template = 'upload_keywords.html'

    if request.GET.get("action",None) == 'upload':
        if 'upgradeKeywords' not in request.session:
            context = {
                "action" : 'upload',
                "errors" : ['There were errors with the upload. Did you enable the cookies in your browser?']
            }
            log("Errore no session. Potrebbe aver provato a ricaricare la pagina dopo l'upload o non aver cookies abilitati", request.user, ctx,2)
            return render(request, template, context)

        upgradeKeywords = request.session.get('upgradeKeywords')
        newKeywords = request.session.get('newKeywords')
        deleteKeywordsPkList = request.session.get('deleteKeywordsPkList')

        deleteKeywords = []
        for pk in deleteKeywordsPkList:
            k = Keyword.objects.get(pk = pk)
            deleteKeywords.append({
                        "keyword" : k.keyword,
                        "asin": k.product.asin,
                        "marketplace" : k.marketplace,
                        "volume" : k.volume,
                        "importance" : k.importance
                    })

        for kw in upgradeKeywords:
            k = Keyword.objects.get(pk = kw['pk'])
            k.volume = kw['volume']
            k.importance = kw['importance']
            k.save()
    
        for kw in newKeywords:
            k = Keyword(
                keyword = kw['keyword'],
                product = Product.objects.get(pk = kw['product'] ),
                marketplace = kw['marketplace'],
                volume = kw['volume'],
                importance = kw['importance']
                )
            k.save()
        
        for pk in deleteKeywordsPkList:
            k = Keyword.objects.get(pk = pk)
            k.delete()

        
        log("Keywords caricate con successo", request.user, ctx,0)
        

        context = {
            "action" : 'upload',
            "upgradeQty" : len(upgradeKeywords),
            "newQty" : len(newKeywords),
            "deleteQty" : len(deleteKeywordsPkList),
            "upgradeKeywords" : upgradeKeywords,
            "newKeywords" : newKeywords,
            "deleteKeywords" : deleteKeywords
        }

        del request.session['upgradeKeywords']
        del request.session['newKeywords']
        del request.session['deleteKeywordsPkList']

        return render(request, template, context)
    

    
    if "keywords_model_file" not in request.FILES:
        return redirect('/analyze/products')
    
    kwsFile = request.FILES["keywords_model_file"]

    mime = mimetypes.guess_type(kwsFile.name)[0]
    
    if mime != 'text/csv':
        return render(request, template, { "errors" : ["File type not correct"]})
    
    kwsFile = pd.read_csv(kwsFile,skiprows=1) #skiprows=1

    errors = []
    newKeywords = []
    upgradeKeywords = []
    deleteKeywordsPkList = []

    dbVariants = Product.objects.filter(user = request.user)
    if dbVariants.count() > 0:
        deleteKeywordsPkList = list(Keyword.objects.filter(product__in = dbVariants).values_list('pk', flat=True))


    for i, row in kwsFile.iterrows():
        rowNumber = i+3

        if row.marketplace not in settings.AVAILABLE_MARKETPLACES:
            errors.append("Marketplace not correct on row " + str(rowNumber))
            continue
        
        variantAsins = str(row.variant_asins).split(",")
        if len(variantAsins) == 0:
            errors.append("No asin on row number " + str(rowNumber))
            continue
        
        try:
            volume = int(row.volume)
        except ValueError:
            volume = 0
        
        try:
            importance = int(row.importance)
        except ValueError:
            importance = 0
        

        dbVariants = []
        for asin in variantAsins:
            asin = asin.strip()
            if asin == "" or asin == "nan":
                errors.append("No ASIN on row " + str(rowNumber))
                continue

            keyword = str(row.keyword).strip()
            if keyword == "" or keyword == "nan":
                errors.append("No keyword on row " + str(rowNumber))
                continue
            try:
                prod = Product.objects.get(asin = asin, marketplace = row.marketplace, user = request.user)
            except ObjectDoesNotExist as e:
                errors.append("Variant with ASIN " + asin + " not found on row " + str(rowNumber))
                continue

            try:
                kwd = Keyword.objects.get(marketplace = row.marketplace, keyword = keyword, product = prod)
                upgradeKeywords.append({
                    "pk" : kwd.pk,
                    "asin": asin,
                    "keyword" : keyword,
                    "marketplace" : row.marketplace,
                    "product" : prod.pk,
                    "volume" : volume,
                    "importance" : importance
                })
                if kwd.pk in deleteKeywordsPkList:
                    deleteKeywordsPkList.remove(kwd.pk)
            except ObjectDoesNotExist as e:
                kwd = Keyword(marketplace = row.marketplace, keyword = keyword, product = prod)
                newKeywords.append({
                    "keyword" : keyword,
                    "asin": asin,
                    "marketplace" : row.marketplace,
                    "product" : prod.pk,
                    "volume" : volume,
                    "importance" : importance
                })
    
    deleteKeywords = []
    for pk in deleteKeywordsPkList:
        k = Keyword.objects.get(pk = pk)
        deleteKeywords.append({
                    "keyword" : k.keyword,
                    "asin": k.product.asin,
                    "marketplace" : k.marketplace,
                    "volume" : k.volume,
                    "importance" : k.importance
                })

    context = {
        "errors" : errors,
        "upgradeQty" : len(upgradeKeywords),
        "newQty" : len(newKeywords),
        "deleteQty" : len(deleteKeywordsPkList),
        "upgradeKeywords" : upgradeKeywords,
        "newKeywords" : newKeywords,
        "deleteKeywords" : deleteKeywords
    }

    if len(errors) == 0:
        request.session['upgradeKeywords'] = upgradeKeywords
        request.session['newKeywords'] = newKeywords
        request.session['deleteKeywordsPkList'] = deleteKeywordsPkList


    return render(request, template, context)


#----------------- FUNCTIONS ----------------


# Controllo il file CSV dei prodotti da caricare e se inEditing == True eseguo gli aggiornamenti sul database
def checkProductsFile(request, inEditing = False):
    print(request.FILES)
    if "products_model_file" not in request.FILES:
        return JsonResponse({"error" : "No file selected"})
    
    prodFile = request.FILES["products_model_file"]


    mime = mimetypes.guess_type(prodFile.name)[0]
    
    if mime != 'text/csv':
        return JsonResponse({ "error" : "File type not correct"})
    
    dbParents = ProductParent.objects.filter(user = request.user)
    dbVariants = Product.objects.filter(user = request.user)
    newParents = []
    newVariants = []

    prodFile = pd.read_csv(prodFile,skiprows=1) #skiprows=1

    for i, row in prodFile.iterrows():
        rowNumber = i+1
        
        if row.marketplace not in settings.AVAILABLE_MARKETPLACES:
            return JsonResponse({ "error" : "Marketplace not correct on row " + str(rowNumber)})
        if row.type != "parent" and row.type != "variant":
            return JsonResponse({ "error" : "Type not correct on row " + str(rowNumber)})
        seller_sku = str(row.seller_sku).strip()
        if seller_sku == "" or seller_sku == 'nan' or len(seller_sku) > 32 :
            return JsonResponse({ "error" : "seller_sku not correct on row " + str(rowNumber)})
        parent_asin = str(row.parent_asin).strip()
        product_asin = str(row.product_asin).strip()
        if product_asin == "" or product_asin == 'nan' or len(product_asin) > 32 :
            return JsonResponse({ "error" : "product_asin not correct on row " + str(rowNumber)})
        
        
        if row.type == "parent":
            if parent_asin != "" and parent_asin != "nan":
                return JsonResponse({ "error" : "A parent product cannot have a parent_asin. On row " + str(rowNumber)})
            newParents.append({
                "marketplace" : row.marketplace,	
                "seller_sku" : seller_sku,	
                "parent_asin" : parent_asin,	
                "product_asin" : product_asin,	
                "type" : row.type
            })
            dbParents = dbParents.exclude(asin = row.product_asin, marketplace = row.marketplace)
        else:
            newVariants.append({
                "marketplace" : row.marketplace,	
                "seller_sku" : seller_sku,	
                "parent_asin" : parent_asin,	
                "product_asin" : product_asin,	
                "type" : row.type
            })
            dbVariants = dbVariants.exclude(asin = row.product_asin, marketplace = row.marketplace)
    
    parentsToDelete = list(dbParents.values("asin","marketplace"))
    variantsToDelete = list(dbVariants.values("asin","marketplace"))

    
    for variant in newVariants:
        if variant["parent_asin"] != "" and variant["parent_asin"] != "nan":
            trovato = False
            for parent in newParents:
                if parent["product_asin"] == variant["parent_asin"]:
                    trovato = True
            if not trovato:
                return JsonResponse({ "error" : "No parent found with ASIN "  + variant["parent_asin"] + " for variant " + variant["product_asin"]})

    #------------------------------- UPDATE DATABASE ---------------------
    if inEditing:
        for variant in dbVariants:
            variant.delete()
        for parent in dbParents:
            parent.delete()

        for parent in newParents:
            try:
                dbProd = ProductParent.objects.get(asin = parent["product_asin"], marketplace = parent["marketplace"], user = request.user)
            except ObjectDoesNotExist as e:
                dbProd = ProductParent(asin = parent["product_asin"], marketplace = parent["marketplace"], user = request.user)
            dbProd.code = parent["seller_sku"]
            dbProd.save()
        
        for variant in newVariants:
            try:
                parent = ProductParent.objects.get(asin = variant["parent_asin"], marketplace = variant["marketplace"], user = request.user)
            except ObjectDoesNotExist as e:
                parent = None

            try:
                dbProd = Product.objects.get(asin = variant["product_asin"], marketplace = variant["marketplace"], user = request.user)
            except ObjectDoesNotExist as e:
                dbProd = Product(asin = variant["product_asin"], marketplace = variant["marketplace"], user = request.user)
            
            dbProd.code = variant["seller_sku"]
            dbProd.parent = parent
            dbProd.save()
    #-----------------------------------------------------------------------


    return JsonResponse({
        "success" : True,
        "parentsToDelete" : parentsToDelete,
        "variantsToDelete" : variantsToDelete
        })

