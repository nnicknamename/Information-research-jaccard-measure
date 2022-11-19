
from django.http import HttpResponse
from django.shortcuts import render
import sys

from Data import * 
database=Database('kxZgDBEwIHkoo9Jd')
indexer=Indexer(file_name="C:/Users/pc/Documents/programming/RI_TP/Implementation/indexer01.pkl")
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
    if request.method == "POST":
        col=database.get_collection('carn')
        query_name = request.POST.get('query', None)
        idx=indexer.get_documents_for_query(query_name)
        print(query_name)
        res=list(col.find({'_id':{"$in":idx.tolist()}}))
        
        return render(request, 'home/home.html', {"results":[list(filter(lambda x:x['_id']==i,res))[0]   for i in idx]})