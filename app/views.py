from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect,HttpRequest,JsonResponse
from django.urls import reverse
from .models import *
import xlrd
import os
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
import xlwt

from datetime import datetime
import pytz


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('app:home'))
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            print("user has logged in \n\n\n")
            return HttpResponseRedirect(reverse('app:home'))
        else:
            print("Somebody logined but failed \n\n\n")
            return HttpResponseRedirect(reverse('app:index'))
    return render(request,'index.html',{})

@login_required
def home(request):
    all_glass_type = GlassType.objects.all()
    all_products = []
    for i in all_glass_type:
        print(i.name)
        n = Product.objects.filter(glass_type=i).values('description').distinct()
        for j in n:
            l=[]
            l.append(i.name)
            l.append(j['description'])
            all_products.append(l)
    print(all_products)
    return render(request,'home.html',{'all_glass_type':all_glass_type,'all_products':all_products})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('app:index'))

@login_required
def productdetails(request,type,desc):
    print(type)
    print(desc)
    total_area = 0;
    all_products = Product.objects.filter(glass_type__name = type).filter(description=desc)
    all_offcut_products = OffCutProduct.objects.filter(glass_type__name = type).filter(description=desc)
    for i in all_products:
        total_area += int(i.size.length) * int(i.size.breadth)*int(i.quantity)
    for i in all_offcut_products:
        total_area += int(i.length) * int(i.breadth)*int(i.quantity)
    total_area = total_area/1000000
    total_area = "%.2f" % total_area
    print(total_area)
    logs = Log.objects.filter(glass_type = type).filter(description=desc).order_by("-pk")[:5]
    context={
        'all_products':all_products,
        'all_offcut_products':all_offcut_products,
        'total_area':total_area,
        'logs':logs,
        'type':type,
        'desc':desc,
    }
    return render(request,'details.html',context)

@login_required
def addlog(request,type,desc):
    all_products = Product.objects.filter(glass_type__name = type).filter(description=desc).order_by("-pk")
    all_offcut_products = OffCutProduct.objects.filter(glass_type__name = type).filter(description=desc)
    if request.method == "POST":
        log_type = request.POST.get('SizeType')
        size = request.POST.get('product').split(",")
        initial_quantity = request.POST.get('initial_quantity')
        print(initial_quantity)
        in_quantity = request.POST.get('in_quantity')
        used_quantity = request.POST.get('used_quantity')
        remark = request.POST.get('remark')
        date = request.POST.get('date')
        if log_type == "Custom":
            length = request.POST.get('length')
            breadth = request.POST.get('breadth')
            op = OffCutProduct.objects.get_or_create(glass_type=GlassType.objects.get(name=type),description=desc,length=length,breadth=breadth)[0]
            print(op)
            initial_quantity = op.quantity
            q = int(op.quantity)
            q += int(in_quantity)
            q -= int(used_quantity)
            print(q)
            op.quantity = str(q)
            op.remarks = remark
            op.save()
            Log.objects.create(glass_type = type,description=desc,size=length+" X "+breadth,initial_quantity=initial_quantity,in_quantity=in_quantity,used_quantity=used_quantity,left_quantity=op.quantity,date=date,user=request.user,remarks=remark)
        else:
            if size[2] == "Offcut":
                p = OffCutProduct.objects.get(glass_type__name=type,description=desc,length=size[0],breadth=size[1])
                print(p.quantity)
                q = int(p.quantity)
                q += int(in_quantity)
                q -= int(used_quantity)
                p.quantity = str(q)
                print(p.quantity)

                p.save()
                Log.objects.create(glass_type = type,description=desc,size=p.length+" X "+p.breadth,initial_quantity=initial_quantity,in_quantity=in_quantity,used_quantity=used_quantity,left_quantity=p.quantity,date=date,user=request.user,remarks=remark)
                if p.quantity == "0":
                    p.delete()
            else:
                p = Product.objects.get(glass_type__name=type,description=desc,size__length=size[0],size__breadth=size[1])
                print(p.quantity)
                q = int(p.quantity)
                q += int(in_quantity)
                q -= int(used_quantity)
                p.quantity = str(q)

                p.save()
                Log.objects.create(glass_type = type,description=desc,size=p.size.__str__(),initial_quantity=initial_quantity,in_quantity=in_quantity,used_quantity=used_quantity,left_quantity=p.quantity,date=date,user=request.user,remarks=remark)
        print("Created")
        return HttpResponseRedirect(reverse('app:viewalllogs',args=(type,desc,)))
    context={
        'all_products':all_products,
        'all_offcut_products':all_offcut_products,
        'type':type,
        'desc':desc,
    }
    return render(request,'addlog.html',context)


def getquantity(request):
    size = request.GET['p'].split(",")
    print(size)
    type = request.GET['type']
    desc = request.GET['desc']
    print(size)
    try:
        if size[2] == "Offcut":
            p = OffCutProduct.objects.get(glass_type__name=type,description=desc,length=size[0],breadth=size[1])
        else:
            p = Product.objects.get(glass_type__name=type,description=desc,size__length=size[0],size__breadth=size[1])
        return JsonResponse(p.quantity,safe=False)
    except Exception as e:
        return JsonResponse("Error")


def getremarks(request):
    details = request.GET['details']
    l = Log.objects.get(pk=int(details))
    return JsonResponse(l.remarks,safe=False)



@login_required
def viewalllogs(request,type,desc):
    logs = Log.objects.filter(glass_type = type).filter(description=desc).order_by("-pk")
    context={
        'logs':logs,
        'type':type,
        'desc':desc,
    }
    return render(request,'alllogs.html',context)



def searchlogs(request):
    data = []
    type = request.GET['type']
    desc = request.GET['desc']
    val = request.GET['val']
    lookups=  Q(size__icontains=val)  | Q(date__icontains=val) | Q(size__startswith=val) | Q(date__startswith=val)
    p = Log.objects.filter(glass_type = type).filter(description=desc).filter(lookups).order_by("-pk").distinct()
    for i in p:
        l = []
        l.append(i.size)
        l.append(i.initial_quantity)
        l.append(i.in_quantity)
        l.append(i.used_quantity)
        l.append(i.left_quantity)
        l.append(i.date)
        data.append(l)
    return JsonResponse(data,safe=False)

@login_required
def exportindividual(request,type,desc):
    header = type + " - " + desc
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="'+header+'.xls"'
    logs = Log.objects.filter(glass_type= type).filter(description=desc).order_by("-pk")

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sheet')

    row_num = 1


    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    ws.write(0, 2, header , font_style)

    columns = ['SIZE', 'INITIAL QUANTITY', 'IN', 'USED', 'LEFT','DATE' ]
    for col_num in range(len(columns)):
        ws.write(1, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = []
    for i in logs:
        l = []
        l.append(i.size)
        l.append(i.initial_quantity)
        l.append(i.in_quantity)
        l.append(i.used_quantity)
        l.append(i.left_quantity)
        l.append(i.date)
        rows.append(l)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


@login_required
def exportalllogs(request):
    user = request.user
    if user.is_authenticated:
        header = "All-logs"
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="'+header+'.xls"'
        logs = Log.objects.all().order_by("-pk")

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet')

        row_num = 1


        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        ws.write(0, 4, header , font_style)

        columns = ['PRODUCT TYPE','DESCRIPTION','SIZE', 'INITIAL QUANTITY', 'IN', 'USED', 'LEFT','DATE' ]
        for col_num in range(len(columns)):
            ws.write(1, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        rows = []
        for i in logs:
            l = []
            l.append(i.glass_type)
            l.append(i.description)
            l.append(i.size)
            l.append(i.initial_quantity)
            l.append(i.in_quantity)
            l.append(i.used_quantity)
            l.append(i.left_quantity)
            l.append(i.date)
            rows.append(l)
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
    return HttpResponseRedirect(reverse('app:index'))

def exportstocklist(request):
    if request.user.is_authenticated:
        header = "STOCK_LIST"
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="'+header+'.csv"'

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Sheet')

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        ws.write(0, 4, header , font_style)

        columns = ['SL.NO.','DESCRIPTION','TOTAL AREA (SQR. MTR.)']

        all_sizes = Size.objects.all().order_by("length")

        for i in all_sizes:
            columns.append(i.__str__())
        for col_num in range(len(columns)):
            ws.write(1, col_num, columns[col_num], font_style)

        all_glass_type = GlassType.objects.all()



        row_num = 2
        c = 0;
        for i in all_glass_type:

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            ws.write(row_num, 4, i.name , font_style)
            row_num = row_num + 1

            n = Product.objects.filter(glass_type=i).values('description').distinct()
            for j in n:
                l=[]
                c = c + 1
                l.append(c)
                l.append(j['description'])
                total_area=0
                for p in Product.objects.filter(glass_type__name = i.name).filter(description=j['description']):
                    total_area += int(p.size.length) * int(p.size.breadth)*int(p.quantity)
                total_area = int(total_area/1000000)
                l.append(total_area)
                for s in all_sizes:
                    try:
                        pr = Product.objects.get(glass_type__name=i.name,description=j['description'],size__length=s.length,size__breadth=s.breadth)
                        l.append(pr.quantity)
                    except Exception as e:
                        l.append(" - ")
                print(l)
                font_style = xlwt.XFStyle()
                for col_num in range(len(l)):
                    print("Writing")
                    ws.write(row_num, col_num, l[col_num], font_style)
                row_num = row_num + 1

        wb.save(response)
        return response
    return HttpResponseRedirect(reverse('app:index'))
