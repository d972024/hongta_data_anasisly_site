from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from sqlalchemy import create_engine
import json
import pandas as pd
eng=create_engine('mysql+pymysql://root:85641212@localhost/ht_site_main')
# Create your views here.
def index(request):
    return render(request, 'test/Table/table_1.html')

def all_data(request):
    print(request.POST.get('myname'))
    page=request.POST.get('page')
    limit=request.POST.get('pageLimit')
    stime=request.POST.get('stime')
    etime=request.POST.get('etime')
    stime=stime + ' 00:00:00' if stime else '2021-01-01 00:00:00'
    if etime:
        etime=etime +' 23:59:59'
    else:
        etime='2021-01-01 23:59:59'

    if limit!='All':
        rows_start=int(page)*int(limit)-int(limit)
        limit=int(limit)
    else:
        rows_start=0
        limit=9999
    data={}
    print(limit,page,stime,etime)
    readdata=pd.read_sql_query('select ah.md5_id,ah.单据编号,ah.产品名称,ah.数量,ah.成本 from getdataapp_fact_act_hscb ah \
                                where (ah.日期 between %(stime)s and %(etime)s) limit 10000;',eng,params={'stime':stime,'etime':etime})
    rows=readdata.iloc[rows_start:(rows_start+limit),:].to_json(orient='records',force_ascii=False)
    data['total']=readdata.shape[0]
    data['rows']=json.loads(rows)
    return JsonResponse(data,safe=True)