
from django.http import HttpResponse
from django.shortcuts import render
import sys

from Data import * 
database=Database('kxZgDBEwIHkoo9Jd')

#from ...Implementation.Data import *
# create a function
def home(request):
    
    return render(
        request,
        'home/home.html',
        {
            'result': 'name',
            'date': 'test'
        }
    )

def search(request):
    """ search function  """
    col=database.get_collection('carn')
    if request.method == "POST":
        query_name = request.POST.get('query', None)
        print(query_name)
        return render(request, 'home/home.html', {"results":col.find({'idx':{'$lt':10}})})