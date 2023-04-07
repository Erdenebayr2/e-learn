from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import random,hashlib
# Create your views here.

def index(request):
    return render(request, 'index.html')

def lesson(request):
    return render(request, 'lesson.html')

def signup(request):
    random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890/$?!', k=4))
    str = random_string
    hasho = hashlib.sha256()
    hasho.update(str.encode('utf8'))
    hex = hasho.hexdigest()
    if request.method == 'POST':
        subject = 'Бүртгэл баталгаажлаа'
        message = 'таны нууц үг бол '+ hex
        sender_email = 'eticket123@gmail.com'
        receiver_email = request.POST.get('receiver_email')
        send_mail(
            subject,
            message,
            sender_email,
            [receiver_email],
            fail_silently=False,
        )
        return HttpResponse('Амжилттай бүртгэгдлээ. Таны '+receiver_email+' хаяг руу нууц үгийг явууллаа.')
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def account(request):
    return render(request, 'account.html')

def contact(request):
    return render(request, 'contact.html')

def chat(request):
    return render(request, 'chat.html')

def asd(request):
    return render(request, 'asd.html')