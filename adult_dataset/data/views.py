from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
# rest
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import AdultData
from . serializers import adultserializers

from django.db import connection

class Homeview(View):
    def get(self, request, *args, **kwargs):
        return render(request,'charts.html',{})


def get_data(request, *args, **kwargs):

    data = AdultData.objects.all()

    data = {
        "sales" : 100,
        "customers" : 10,
    }
    return JsonResponse(data)



class ChartData(APIView):
    authentication_classes =[]
    permission_classes =[]

    def get(self, request, format=None):
        # import pdb; pdb.set_trace()

        # distribution of number of males and females using raw sql query

        cursor = connection.cursor()
        cursor.execute('''SELECT count(*) FROM data_adultdata where sex=' Male';''')
        male_count = cursor.fetchone()
        cursor.execute('''SELECT count(*) FROM data_adultdata where sex=' Female';''')
        female_count = cursor.fetchone()

        # pass data as json format

        values  = [ male_count , female_count]
        labels = ["male", "female"]
        d = {
            "labels" : labels,
            "values" : values,
        }

        # no of relationship data
        wife_count = AdultData.objects.filter(relationship__startswith=' Wife').count()

        child_count = AdultData.objects.filter(relationship__startswith=' Own-child').count()
        husband_count = AdultData.objects.filter(relationship__startswith=' Husband').count()
        nif_count = AdultData.objects.filter(relationship__startswith=' Not-in-family').count()
        relativ_count = AdultData.objects.filter(relationship__startswith=' Other-relative').count()
        single_count = AdultData.objects.filter(relationship__startswith=' Unmarried').count()

        labels_of_relations = ["Wife", "Own-child", "Husband", "Not-in-family", "Other-relative", "Unmarried"]
        count_of_relations  = [ wife_count , child_count, husband_count, nif_count , relativ_count,single_count ]

        e = {
            "labels" : labels_of_relations,
            "values" : count_of_relations,
            }
        # adult_data = AdultData.objects.all()
        # serializer = adultserializers(adult_data, many=True)
        # data = serializer.data
        return Response([d,e])
