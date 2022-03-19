import json
from .models import form,responses
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User, auth, AnonymousUser
from django.shortcuts import render, redirect


# Create your views here.
from django.http import HttpResponse
def index(request):
    if type(request.user) is AnonymousUser or not request.user.is_authenticated:
        homi = {}
        return render(request,'myforms/home.html',homi)
    else:
        frm = form.objects.filter(user_id = request.user)
        resp = responses.objects.filter(user_id = request.user)
        print(len(frm),len(resp))
        homi = {'forms':frm,'resps':resp,'numfrm':len(frm),'numresp':len(resp)}
        return render(request,'myforms/home.html',homi)

def create(request):
    return render(request,'myforms/create.html')

def previewresponse(request,id):
    resp = responses.objects.get(id = id)
    homi = {'resps':resp.responses,'title':resp.form_id.title,'name':resp.form_id.user_id.username}
    print(homi)
    return render(request,'myforms/preview.html',homi)

def previewform(request, id):
    frm = form.objects.get(id=id)
    homi = {'b': frm.questions, 'title': frm.title, 'user': frm.user_id.username}
    return render(request, 'myforms/previewform.html', homi)

def filled(request,id):
    global fillid
    if request.method == "POST":
        frm = form.objects.get(id=fillid)
        obj = frm.questions["questions"]
        for x in obj:
            ANS = request.POST.getlist(x["question"], '')
            x["answers"] = ANS
        jsobj = {"responses":obj}
        alli = json.loads(json.dumps(jsobj))
        resp = responses(user_id = request.user,form_id = frm,responses = alli)
        resp.save()
        return redirect('/myforms')
    frm = form.objects.get(id = id)
    fillid = id
    print(frm.title)
    homi = {'b':frm.questions,'title':frm.title,'user':frm.user_id.username}
    return render(request,'myforms/fill.html',homi)

def formcreated(request):
    global JQS
    global FORM
    if request.method == "POST":
        QS = request.POST.get('main', '')
        title = request.POST.get('tit', '')
        JQS = json.loads(QS)
        FORM = form(user_id = request.user,title = title,questions=JQS)
        FORM.save()

    messages.info(request, FORM.id)
    return redirect('/myforms/create')

def login(request):
    global userpass
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        userpass = password

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            print("success")
            return redirect('/myforms')
        else:
            messages.info(request, 'invalid credentials')
    return render(request, 'myforms/login.html')

def signin(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')


        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username taken')
                return redirect('/myforms/signin')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email taken')
                return redirect('/myforms/signin')
            else:
               user = User.objects.create_user(username=username,password=password1,email=email)
               user.save()
               auth.login(request,user)
               print(user)
        else:
            messages.info(request, 'password not matching')
        return redirect('/myforms/')
    else:
        return render(request,'myforms/signin.html')

def logOut(request):
    auth.logout(request)
    return redirect('/myforms')
