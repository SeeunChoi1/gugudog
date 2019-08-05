from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import AddForm
from .models import Service, GuDogService, GuDog, Zzim, ZzimService
from django.contrib.auth.decorators import login_required
from dal import autocomplete
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
import json

# Create your views here.
@login_required(login_url='signup/')
def home(request):

    gudog = GuDogService.objects.filter(user=request.user)

    context = {
        'gudog': gudog,
    }
    return render(request, 'home.html', context)

@login_required(login_url='signup/')
def service_all(request):
    services = Service.objects.all()

    context = {
        'services': services,
    }
    return render(request, 'service_all.html', context)

@login_required(login_url='signup/')
def recommendation(request):
    return render(request, 'recommendation.html')


def signup(request):
    return render(request, 'registration/signup.html')


def logout(request):
    auth.logout(request)
    return redirect('signup')

@login_required(login_url='signup/')
def add(request):
    model = GuDogService.objects.all()
    form = AddForm()
    context = {
        'form': form,
        'models': model,
    }

    if request.method == "POST": 
        try:
            service_pk = request.POST.get('pk', False)
            service = get_object_or_404(Service, pk=service_pk)
            print(service)
            print(service.price)
            return HttpResponse(json.dumps(service.price))
        except:  
            gudog_added, created = GuDogService.objects.get_or_create(
                user=request.user,
                service=Service.objects.get(pk=request.POST['service']),
                register_date=request.POST['register_date']
            )
            
            print(gudog_added)
            gudog_qs = GuDog.objects.filter(user=request.user)
            if gudog_qs.exists():
                gudog = gudog_qs[0]
                # 이미 해당 서비스를 구독했으면
                if gudog.services.filter(service__pk=gudog_added.service.pk).exists():
                    gudog_added.delete()
                    return redirect('add')
                else:
                    gudog.services.add(gudog_added)
                    service = Service.objects.get(pk=gudog_added.service.pk)
                    service.gudog_users.add(request.user)
                    return redirect('home')
            else:
                gudog_added.save()
                gudog = GuDog.objects.create(user=request.user)
                gudog.services.add(gudog_added)
                service = Service.objects.get(pk=gudog_added.service.pk)
                service.gudog_users.add(request.user)
                return redirect('home')
    else:
        # GET 방식으로 요청이 들어오면
        # ajax 요청이면 try 실행
        # try:
        #     pk = request.GET.get('pk')
        #     service = get_object_or_404(Service, pk=pk)
        #     print(service)
        #     context['service']=service
        #     print(context.service.price)
        #     return JsonResponse(context['service'])
        # # ajax 요청이 아니면 그냥 add 페이지 render
        # except:
        return render(request, 'add.html', context)

@login_required(login_url='signup/')

def delete_service(request, gudog_service_pk, model_service_pk):
    deletingService = GuDogService.objects.get(pk=gudog_service_pk)

    service = Service.objects.get(pk=model_service_pk)

    service.gudog_users.remove(request.user)
    service.zzim_users.remove(request.user)

    deletingService.delete()
    return redirect('home')

@login_required(login_url='signup/')
def service_detail(request, service_pk):
    service = Service.objects.get(pk=service_pk)
    context = {
        'service': service,
    }
    if request.user in service.gudog_users.all():
        context['isGuDoged'] = "구독하고 있는 서비스에요!"
    elif request.user in service.zzim_users.all():
        context['isZzimed'] = "찜한 구독 서비스에요!"
    
    return render(request, 'service_detail.html', context)

def zzim(request):
    context = {
        'zzim':"찜했어용",
    }
    if request.method == "POST":
        pk = request.POST.get('pk', None)
        service = get_object_or_404(Service, pk=pk)
        zzim_service, created = ZzimService.objects.get_or_create(
            user=request.user,
            service = Service.objects.get(pk=request.POST.get('pk')),
        )

        if not created:
            zzim_service.delete()
            context['zzim']="찜"
            return HttpResponse(json.dumps(context))
    
        zzim_qs = Zzim.objects.filter(user=request.user)
        if zzim_qs.exists():
            zzim = zzim_qs[0]
            if zzim.services.filter(service__pk=zzim_service.service.pk):
                zzim_service.delete()
                context['zzim']="찜"
                return HttpResponse(json.dumps(context))
            else:
                zzim_service.save()
                zzim.services.add(zzim_service)
                service = Service.objects.get(pk=zzim_service.service.pk)
                service.zzim_users.add(request.user)
                return HttpResponse(json.dumps(context))
        else:
            zzim_service.save()
            zzim = Zzim.objects.create(user=request.user)
            zzim.services.add(zzim_service)
            service = Service.objects.get(pk=zzim_service.service.pk)
            service.zzim_users.add(request.user)
    
    return HttpResponse(json.dumps(context))


def mp(request):
    zzim = ZzimService.objects.filter(user=request.user)
    context = {
        'zzim': zzim,
    }
    return render(request, "mp.html", context)

@login_required(login_url='signup/')
def delete_zzim(request, zzim_service_pk, model_service_pk):
    deletingService = ZzimService.objects.get(pk=zzim_service_pk)
    deletingService.delete()

    service = Service.objects.get(pk=model_service_pk)
    service.zzim_users.remove(request.user)

    return redirect('home')