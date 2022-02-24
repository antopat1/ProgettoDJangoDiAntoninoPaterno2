import os.path
from django.shortcuts import render
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import FormRegistrazionUser, WriteNewsModelForm,ChoiceForm,FormJournalist,FormCountwords
from .models import News
from api.utils import sendTransaction
import hashlib
import json
from .models import News,LoggerUser
from django.utils import timezone
from django.utils.timezone import now ,datetime, timedelta
from ipware import get_client_ip
from django.http import JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
import shutil
from collections import Counter
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

def homepage(request):
    return render(request,"access_register/homepage.html")


def registrazion(request):
    if request.method == "POST":
        form = FormRegistrazionUser(request.POST)
        try:
            if form.is_valid():
                username=form.cleaned_data["username"]
                email = form.cleaned_data["email"]
                password = form.cleaned_data["password"]
                User.objects.create_user(username=username,password=password,email=email)
            #user = authenticate(username=username,password=password) # qualora volessi loggarmi direttamente
            #login(request,user)
                return HttpResponse('"<h1>Utente creato con successo!</h1><a class="nav-link" href="/">Torna alla Homepage!</a>"')
            #avrei potuto usare anche un httpredirect per pagine più complesse puntando ad un url e relativa view
        except:
            return HttpResponse('"<h1>ALERT! Attenzione non hai inserito tutti i dati necessari per la creazione! </h1><a class="nav-link" href="/registrazione/"><br><h2> Ripeti operazione</h2>"')


    else:
        form = FormRegistrazionUser()
    context = {"form": form}
    return render(request, "registration/registrazione.html", context)

@staff_member_required()
def news_view(request):

    if request.method=="POST":
        form=WriteNewsModelForm(request.POST)

        if form.is_valid():
            new_message=form.save(commit=False)
            new_message.user=request.user


            baseJs = {
                'title': new_message.title,
                'content': new_message.content,
             }
            JsonFile=json.dumps(baseJs)
            jsonFile = open("data.json", "w")
            jsonFile.write(JsonFile)
            jsonFile.close()
            new_message.hash = hashlib.sha256(JsonFile.encode('utf-8')).hexdigest()
            new_message.txId = sendTransaction(new_message.hash)
            new_message.save()
            return HttpResponse ('"<h1>Il tuo articolo giornalistico è stato registrato con successo!<br> Il suo identificativo di ricerca è {}</h1>'.format(new_message.id)+'<a class="nav-link" href="/">Torna alla Homepage!</a>"')
    else:
        form=WriteNewsModelForm()

    context = {"form":form}
    return render(request,"access_register/form1.html",context)


def log_home(request):
    ip_u, is_routable = get_client_ip(request)
    new_access=LoggerUser(user=request.user,datetime=timezone.now(),ip_user=ip_u)
    new_access.save(force_insert=True)
    records_access_log=LoggerUser.objects.filter().values()
    if len(records_access_log) == 1:
        return render(request,"access_register/homepage.html")
    else:
        if records_access_log[len(records_access_log)-1]['ip_user'] == records_access_log[len(records_access_log)-2]['ip_user']:
            return render(request, "access_register/homepage.html")
        elif records_access_log[len(records_access_log) - 1]['user_id'] == records_access_log[len(records_access_log) - 2]['user_id']:
            return HttpResponse('"<h1>ALERT! : IP addess del precedente log di accesso cambiato per lo user corrente! </h1><a class="nav-link" href="/">Torna alla Homepage!</a>"')
        else:
            return render(request, "access_register/homepage.html")

@login_required()
def outJson_search(request,id_search):
    response = []
    exist=False
    news_serch=News.objects.filter()
    for news in news_serch:
        if news.id == id_search:
            exist = True
            response.append(
            {
              "id":news.id,
              "user": news.user.username,
              "datetime":news.datetime,
              "title": news.title,
              "content": news.content,
              "hash": news.hash,
              "txId": news.txId,
             }
         )
    if exist:
        return JsonResponse(response, safe=False,json_dumps_params={'indent': 3})
    else:
        return HttpResponse('"<h1>ALERT! Non esiste alcun articolo con il cui ID corrisponde alla ricerca </h1><a class="nav-link" href="/chose_Idsearch">Inserisci solo ID di articoli registrati</a>"')

@login_required()
def download_file(request,id_search):
    exist = False
    news_jH = News.objects.filter()
    for sing_Jserch in news_jH:
        if sing_Jserch.id == id_search:
            exist = True
            baseJs = {
                'title': sing_Jserch.title,
                'content': sing_Jserch.content,
            }
            JsonFile = json.dumps(baseJs)
            jsonFile = open("data.json", "w")
            jsonFile.write(JsonFile)
            jsonFile.close()
            filename = "/data.json"
            base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            original = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + filename
            target = base + '/FILE/' + filename
            shutil.move(original, target)
    if exist:
        base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename="data.json"
        filepath= base_dir + '/FILE/' + filename
        thefile = filepath
        filename=os.path.basename(thefile)
        chunk_size=8192
        response=StreamingHttpResponse(FileWrapper(open(thefile,'rb'),chunk_size),content_type=mimetypes.guess_type(thefile)[0])
        response['Content-Lenghth']=os.path.getsize(thefile)
        response['Content-Disposition']="Attachment;filename=%s" % filename
        return response
    else:
        return HttpResponse('"<h1>ALERT! Non esiste alcun articolo con il cui ID corrisponde alla ricerca </h1><a class="nav-link" href="/chose_Idsearch">Inserisci solo ID di articoli registrati</a>"')


class newsListCBV(ListView): # le classi ereditano dalla classe base ListView
    model=News
    template_name="art_list.html"
    ordering = ['-datetime'] #definisco l 'ordinamento richiesto dal progetto
    paginate_by = 5

class numNewsListCBV(DetailView):
    model=User
    template_name="art_singUser.html"


@login_required()
def outJson_lastH(request):
    response = []
    dt = now()
    newsH=News.objects.filter(datetime__range=(dt-timedelta(hours=1), dt))  #
    for news in newsH:
            response.append(
             {
              "id":f"{news.id}",
              "user":f"{news.user.username}",
              "datetime":f"{news.datetime}",
              "title":f"{news.title}",
              "content":f"{news.content}",
              "hash":f"{ news.hash}",
              "txId":f"{news.txId}",
             }
         )
    return JsonResponse(response, safe=False,json_dumps_params={'indent': 3})

@login_required()
def chose_Idsearch(request):

    if request.method=="POST":
        form_id=ChoiceForm(request.POST)

        if form_id.is_valid():
            choice=form_id.save(commit=False)
            #choice.save()
            a=str(choice.articleIdCode)
            b=str(choice.typeOutJson)
            if b=='HTML':
                return HttpResponseRedirect('/outJson_search/'+a+"/")
            elif b=='FILE':
                return HttpResponseRedirect('/download_file/' +a+ "/")
            else:
                return HttpResponse('"<h1>ALERT! Attenzione scelta NON valida.<br> Inserire HTML per outputJson su Browser o inserire FILE per download Json </h1><a class="nav-link" href="/chose_Idsearch">Reinserisci combinazione corretta.</a>"')

    else:
        form_id=ChoiceForm()

    context = {"form_id":form_id}
    return render(request,"access_register/form2.html",context)

@login_required()
def journalist_id_search(request):

    if request.method=="POST":
        form_j_id=FormJournalist(request.POST)

        if form_j_id.is_valid():
            choice=form_j_id.save(commit=False)
            #choice.save()
            a=str(choice.journalistId)
            all_user = User.objects.filter()
            exist=False
            for user in all_user:
                if str(user.id) == a:
                    exist = True
            if exist:
                return HttpResponseRedirect('/news_x_user_id/'+a+"/")
            else:
                return HttpResponse('"<h1>ALERT! Attenzione nessun Giornalista ha l ID indicato<br></a><a class="nav-link" href="/journalist_id_search/">Reinserisci Id -> solo giornalisti in archivio</a>"')


    else:
        form_j_id=FormJournalist()

    context = {"form_j_id":form_j_id}
    return render(request,"access_register/form3.html",context)

@staff_member_required()
def count_art_ripetition(request, word):

    art_estr = News.objects.all()
    unic_string=" "

    for sing_art in art_estr:
        unic_string+=sing_art.content

    conteggio=unic_string.upper().count(word.upper())

    rend_contex={'word': word, 'conteggio' : conteggio}

    return render(request, 'count_repetitions.html', rend_contex)

@staff_member_required()
def word_in_item(request):

    if request.method=="POST":
        form_w=FormCountwords(request.POST)

        if form_w.is_valid():
            choice=form_w.save(commit=False)
            w=str(choice.sWord)
            return HttpResponseRedirect('/conta_ripetizioni/'+w+"/")

    else:
        form_w=FormCountwords()

    context = {"form_w":form_w}
    return render(request,"access_register/form4.html",context)

@login_required()
def news_x_journ(request):
    all_news=News.objects.all()
    journalists_list=[]
    for news in all_news:
        journalists_list.append(news.user)

    contUser=dict(Counter(journalists_list))
    context={'contUser': contUser }
    return render(request, 'artXuser.html',context )

