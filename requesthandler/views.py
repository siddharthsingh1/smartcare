# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.views.decorators.csrf import csrf_exempt
from requesthandler.models import patient_data , patient_medicines
from django.shortcuts import render
from twilio.rest import Client
from django.shortcuts import render
from django.views.generic import TemplateView


account_sid = "AC1b439dccd6eadc77a2820db708b67b95"
auth_token = "a4e5dad158364490ed18f30670006438"

from django.http import HttpResponse , HttpResponseServerError


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@csrf_exempt
def save_data(request):
    print("test")
    if request.method == 'POST':

        json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
    try:
        name = json_data['name']
        email = json_data['email']
        age = json_data['age']
        device_id = json_data['device_id']
        patient_relatives = json_data['patient_relatives']

        data_to_insert = patient_data(patient_name = name , device_id = device_id ,
                                      patient_email = email , patient_age = age,
                                      patient_relatives = patient_relatives)
        data_to_insert.save()
        return HttpResponse("success!")

    except KeyError:
        HttpResponseServerError("Malformed data!")
    except Exception:
        HttpResponse("Error storing data")
    HttpResponse("Got json data")


@csrf_exempt
def save_medicines_data(request):

    if request.method == 'POST':

        json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
    try:
        device_id = json_data['device_id']
        medicines = json_data['medicines']

        data_to_insert = patient_medicines(patient_device_id = device_id , medicines = medicines)
        data_to_insert.save()
        return HttpResponse("success!")

    except KeyError:
        HttpResponseServerError("Malformed data!")
    except Exception:
        HttpResponse("Error storing data")
    HttpResponse("Got json")

@csrf_exempt
def save_medicines_data2(request):

    if request.method == 'POST':

        device_id = request.POST['device_id']
        medicines = request.POST['medicines']
        dose = request.POST['dose']
        time = request.POST['time']
        color = request.POST['color']
        medicines = medicines+':'+dose+':'+time+':'+color
        data_to_insert = patient_medicines(patient_device_id = device_id , medicines = medicines)
        data_to_insert.save()
        return HttpResponse("success!")


    HttpResponse("Got json")




@csrf_exempt
def get_user_list(request):
    lst = []

    for e in patient_data.objects.all():
        result = {}
        result['patient_name'] =  e.patient_name
        result['patient_device_id']= e.device_id
        lst.append(result)

    print(lst)

    return HttpResponse(lst)

@csrf_exempt
def get_user_medicines(request):
    lst = []

    if request.method == 'POST':

        json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
    try:
        device_id = json_data['device_id']

        for e in patient_medicines.objects.filter(patient_device_id=device_id):
            result = {}
            result['medicines'] = e.medicines
            lst.append(result)

        print(lst)
        return HttpResponse(lst)

    except KeyError:
        HttpResponseServerError("Malformed data!")
    except Exception:
        HttpResponse("Error storing data")
    HttpResponse("Got json")



    return HttpResponse(lst)

@csrf_exempt
def get_user_medicines_get(request):
    lst = []

    if request.GET.get('device_id'):
        device_id = request.GET['device_id']

        for e in patient_medicines.objects.filter(patient_device_id=device_id):
            result = {}
            result['medicines'] = e.medicines
            lst.append(result)

        print(lst)
        return HttpResponse(json.dumps(lst))





    return HttpResponse(lst)



@csrf_exempt
def send_alert2(request):
    client = Client(account_sid, auth_token)

    if request.GET.get('device_id'):
        device_id = request.GET['device_id']
        print(device_id)
        for e in patient_data.objects.all():
            # print(e.patient_relatives)
            if(e.patient_relatives):
                x = e.patient_relatives

                for number in str(x).split(','):
                    if(number != ""):
                        client.messages.create(to=str(number), from_="+13054401606",
                                               body="your grand father has not taken the medicine!")

        return HttpResponse(json.dumps(["success"]))


@csrf_exempt
def send_alert(request):
    client = Client(account_sid, auth_token)

    if request.method == 'POST':

        json_data = json.loads(request.body) # request.raw_post_data w/ Django < 1.4
    try:
        device_id = json_data['device_id']
        print(device_id)
        for e in patient_data.objects.all():
            # print(e.patient_relatives)
            if(e.patient_relatives):
                x = e.patient_relatives

                for number in str(x).split(','):
                    if(number != ""):
                        client.messages.create(to=str(number), from_="+13054401606", body="Hello from Python!")

        return HttpResponse("success")

    except KeyError as ex:
        print(ex)
        HttpResponseServerError("Malformed data!")
    except Exception as ex:
        print(ex)
        HttpResponse("Error storing data")
    HttpResponse("Got json")

class list_users(TemplateView):
    def get(self, request, **kwargs):
        users = patient_data.objects.all()
        stu = {
            "users_data": users
        }
        return render(request,'index.html',stu)

class add_user_prescription(TemplateView):
    def get(self, request, **kwargs):
        stu={}
        if request.GET.get('device_id'):
            device_id = request.GET['device_id']


        return render(request,'addpresciption.html',{'device_id':device_id})


class user_details(TemplateView):
    def get(self, request, **kwargs):
        if request.GET.get('device_id'):
            device_id = request.GET['device_id']
            user_schedule = patient_medicines.objects.filter(patient_device_id=device_id)[0]
            stu = []
            for medicine in str(user_schedule.medicines).split(','):
                temp_list = {}
                temp_list['name'] = str(medicine).split(':')[0]
                temp_list['dose'] = medicine.split(':')[1]
                temp_list['time'] = medicine.split(':')[2]
                temp_list['color'] = medicine.split(':')[3]

                temp_list['device_id'] = device_id

                stu.append(temp_list)
            print(device_id+ "sdsdsadasd")

            return render(request, 'schedule.html', {'stu':stu , 'x':device_id } )
        else:
            message = 'You submitted nothing!'
            return HttpResponse("id required")
