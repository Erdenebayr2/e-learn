from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.http import HttpResponseBadRequest,HttpResponse
from django.contrib import messages
import random,hashlib,os
from django.conf import settings
import psycopg2
# Create your views here.

def delete(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        con = psycopg2.connect(
            host='localhost', 
            port='5432',
            database='o-learn',
            user='postgres',
            password='eba.1117',
        )
        cur = con.cursor()
        cur.execute('DELETE FROM el_video WHERE t_vid=%s', [id])
        con.commit()
        cur.close()
        return redirect('lesson')
    else:
        return HttpResponseBadRequest()

def index(request):
    return render(request, 'index.html')

def handle_uploaded_file(file , name):
    file_name = file.name
    file_path = os.path.join(settings.MEDIA_ROOT, name+".mp4")
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def lupdate(request):
    if request.method == 'POST':
        update = request.POST['lupdate']
        return redirect('lesson')
    return render(request, 'update.html')

def lesson(request):
    if request.method == 'POST':
        vtitle = request.POST['vtitle']
        file = request.FILES.get('video')
        video = file.name
        desc = request.POST['desc']
        m_type = request.POST.get('t_type')
        el_id = request.session['uname']
        context = {
                "lid": el_id
            }
        if file:
            handle_uploaded_file(file , vtitle)
            con = psycopg2.connect(
                host='localhost', 
                port='5432',
                database='o-learn',
                user='postgres',
                password='eba.1117',
                )
        curs = con.cursor()
        curs.execute('SELECT * FROM "el_users" WHERE el_id=%s ',[el_id])
        xp = curs.fetchall()
        xp = list(xp)
        context['name']=xp[0][2]
        content = context['name']
        print(content)
        cur = con.cursor()
        cur.execute('INSERT INTO "el_video" (t_vtitle,t_vdes,t_video,t_type,t_tusers) VALUES (%s,%s,%s,%s,%s)',[vtitle,desc,vtitle,m_type,content])
        con.commit()
        cur.close()
        return redirect('lesson')  
    else:
        el_id = request.session['uname']
        context = {
            'data' : '',
            'lid' : el_id
        }
        con = psycopg2.connect(
                host='localhost', 
                port='5432',
                database='o-learn',
                user='postgres',
                password='eba.1117',
                )
        cur = con.cursor()
        cur.execute('SELECT * FROM el_video ')
        curs = con.cursor()
        curs.execute('SELECT * FROM "el_users" WHERE el_id=%s ',[el_id])
        xp = curs.fetchall()
        xp = list(xp)
        context['name']=xp[0][2]    
        context['data'] = cur.fetchall()

        return render(request, 'lesson.html' , context=context)

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
            cur.execute('SELECT el_id,el_last  FROM "el_users" WHERE el_name=%s AND el_password=%s',[uname,passw])
            xp = cur.fetchall()
            xp = list(xp)
            print(xp[0][1])
            # user = authenticate(request,uname=uname,passw=passw)
            if len(xp) == 1:
                request.session['uname'] = xp[0][0]
                if xp[0][1] == 'Багш':
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

def learnl(request):
    if request.method == 'GET':
        con = psycopg2.connect(
                    host='localhost', 
                    port='5432',
                    database='o-learn',
                    user='postgres',
                    password='eba.1117',
                    )
        cur = con.cursor()    
        torol = request.GET.get('torol')
        cur.execute(f'SELECT * FROM el_video WHERE t_type = {torol}')
        context = {
            'data' : ''
        }
        context['data'] = cur.fetchall()
        return render(request, 'learn-l.html', context=context)

def forget(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        femail = request.POST.get('femail')
        con = psycopg2.connect(
            host='localhost', 
            port='5432',
            database='o-learn',
            user='postgres',
            password='eba.1117',
            )
        cur = con.cursor()
        cur.execute('SELECT count(el_users) FROM el_users WHERE el_name = %s AND el_mail = %s',[fname,femail])
        x = list(cur.fetchone())
        print(x[0])
        if x[0] == 1:
            return redirect('forget2')
    return render(request, 'forget.html')

def forget2(request):
    if request.method == 'POST':
        npass = request.POST.get('npass')
        rname = request.POST.get('rname')
        con = psycopg2.connect(
            host='localhost', 
            port='5432',
            database='o-learn',
            user='postgres',
            password='eba.1117',
            )
        cur = con.cursor()
        cur.execute('UPDATE "el_users" SET el_password=%s WHERE el_name=%s',[npass,rname])
        con.commit()
        return redirect('log_in')
    return render(request, 'forget2.html')

def blog(request):
    return render(request, 'blog.html')