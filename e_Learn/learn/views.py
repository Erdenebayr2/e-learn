from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import random,hashlib
from django.contrib.auth.decorators import login_required
import psycopg2
# Create your views here.

def index(request):
    return render(request, 'index.html')

def lesson(request):
    return render(request, 'lesson.html')

def signup(request):
    if request.session.get('uname'):
        return redirect('dashboard')
    else:
        random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890/$?!', k=4))
        str = random_string
        hasho = hashlib.sha256()
        hasho.update(str.encode('utf8'))
        hex = hasho.hexdigest()
        hex = hex[:6]
        if request.method == 'POST':
            subject = 'Бүртгэл баталгаажлаа'
            message = 'таны нууц үг бол '+ hex
            sender_email = 'eticket123@gmail.com'
            receiver_email = request.POST.get('receiver_email')
            username = request.POST['username']
            lastname = request.POST['lastname']
            password = hex
            send_mail(
                subject,
                message,
                sender_email,
                [receiver_email],
                fail_silently=False,
            )
            con = psycopg2.connect(
                host='localhost', 
                port='5432',
                database='o-learn',
                user='postgres',
                password='eba.1117',
                )
            cur = con.cursor()
            cur.execute('INSERT INTO "el_users" (el_last,el_name,el_mail,el_password) VALUES (%s, %s,%s,%s)',[lastname, username,receiver_email,password])
            con.commit()
            # return HttpResponse('Амжилттай бүртгэгдлээ. Таны '+receiver_email+' хаяг руу нууц үгийг явууллаа.')
            return redirect('log_in')
        return render(request, 'signup.html')

def log_in(request):
    if request.session.get('uname'):
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            uname = request.POST.get('uname')
            passw = request.POST.get('password')
            con = psycopg2.connect(
                host='localhost', 
                port='5432',
                database='o-learn',
                user='postgres',
                password='eba.1117',
                )
            cur = con.cursor()
            cur.execute('SELECT el_id  FROM "el_users" WHERE el_name=%s AND el_password=%s',[uname,passw])
            xp = cur.fetchall()
            xp = list(xp)
            print()
            # user = authenticate(request,uname=uname,passw=passw)
            if len(xp) == 1:
                request.session['uname'] = xp[0][0]
                if xp[0][0] == 1:
                    return redirect('teacher')
                else:
                    return redirect('dashboard')
            else:
                return redirect('')

        else:
            messages.error(request, 'Invalid username or password.')

        return render(request, 'login.html')

def account(request):
    return render(request, 'account.html')

def contact(request):
    return render(request, 'contact.html')

def teacher(request):
    return render(request, 'teacher.html')


def dashboard(request):
        if request.session.get('uname'):
            el_id = request.session['uname']
            context = {
                "lid": el_id
            }
            con = psycopg2.connect(
                host='localhost', 
                port='5432',
                database='o-learn',
                user='postgres',
                password='eba.1117',
                )
            cur = con.cursor()
            cur.execute('SELECT * FROM "el_users" WHERE el_id=%s ',[el_id])
            xp = cur.fetchall()
            xp = list(xp)
            context['name']=xp[0][2]
            return render(request, 'dashboard.html',context = context)
        else:
            return redirect('log_in')
def log_out(request):
    del request.session['uname']
    logout(request)
    return redirect('log_in')

