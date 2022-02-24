"""news_notarization URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from access_register.views import homepage,registrazion,news_view,log_home,outJson_search,download_file,newsListCBV,numNewsListCBV,outJson_lastH,chose_Idsearch,journalist_id_search,count_art_ripetition,word_in_item,news_x_journ
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name="homepage"),
    path('registrazione/', registrazion, name="registrazione"),
#avendo importato le viste dal django.contrib.auth, dall'alias posso istanziare delle pagine.html che rendono possibile il reset password da terminale
    path('account/password_reset/',
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    #inizio a definire gli url che richiamano le view grazie alle quali elaboro i requisiti del progetto
    path('scrivi_post/', news_view, name="news_view"),
    path('log_home/', log_home , name="log_home"),
    path('outJson_search/<int:id_search>/', outJson_search , name="outJson_search"),
    path('outJson_lastH/', outJson_lastH , name="outJson_lastH"),
    path('visualizza_post/', newsListCBV.as_view(), name="lista_news"),
    path('news_x_user_id/<int:pk>/', numNewsListCBV.as_view(), name="dettagli_news"),
    path('download_file/<int:id_search>/', download_file , name="download_file"),
    path('chose_Idsearch/', chose_Idsearch , name="chose_Idsearch"),
    path('journalist_id_search/', journalist_id_search , name="journalist_id_search"),
    path('conta_ripetizioni/<str:word>/', count_art_ripetition , name="count_art_ripetition"),
    path('word_in_item/', word_in_item , name="word_in_item"),
    path('news_x_journ/', news_x_journ , name="news_x_journ"),

]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]