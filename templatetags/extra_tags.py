from django import template
import os
import uuid                                                                                                       
from django.conf import settings  
register = template.Library()

@register.filter
def get_attr(obj,attr): 
    """Get the object's field from string"""
    return getattr(obj,attr)

@register.filter
def get_item(dictionary, key):
    """Per accedere al campo di un dict senza poter usare [key]"""
    return dictionary.get(key)

@register.filter
def get_table_item(dictionary, key):
    """Per accedere al campo di un dict senza poter usare [key]"""
    item = dictionary.get(key)
    #if item is None: return ''
    return item

@register.simple_tag(name='cache_bust')                                                                                                  
def cache_bust():                                                                                                                        

    if settings.DEBUG:                                                                                                                   
        version = uuid.uuid1()                                                                                                           
    else:                                                                                                                                
        version = os.environ.get('PROJECT_VERSION')                                                                                       
        if version is None:                                                                                                              
            version = '1'                                                                                                                

    return '__v__={version}'.format(version=version)



