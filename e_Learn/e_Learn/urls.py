from django.contrib import admin
from django.urls import path
from learn import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index , name='index'),
    path('lesson/', views.lesson, name='lesson'),
    path('signup/', views.signup, name='signup'),	
    path('account/',views.account, name='account'),
    path('teacher/',views.teacher, name='teacher'),
    path('contact/',views.contact, name='contact'),
    path('log_in/', views.log_in, name='log_in'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_out/', views.log_out, name='log_out'),
    path('learn-l/', views.learnl, name='learn_l'), 
    path('forget/', views.forget, name='forget'),
    path('forget2/', views.forget2, name='forget2'),
    path('blog/', views.blog, name='blog'),
    path('delete/', views.delete, name='delete'),
    # path('admin/', admin.site.urls)
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
