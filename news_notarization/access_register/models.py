from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class News(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE,related_name='elenco')  #related name mi serve per visualizzare eventualmente tutte le notizie di un user per chiave
    datetime=models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=50)
    content=models.TextField()
    hash = models.CharField(max_length=32, default=None, null=True)
    txId = models.CharField(max_length=66, default=None, null=True)
    class Meta:
        verbose_name= "notizia"
        verbose_name_plural = "notizie"
    def get_absolute_url(self):
        return reverse("dettagli_news",kwargs={"pk":self.user.pk})

class LoggerUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sequenzaLogUser')
    datetime = models.DateTimeField(auto_now_add=True)
    ip_user=models.TextField(default="0.0.0.0")
    class Meta:
        verbose_name= "Utente_log"
        verbose_name_plural = "Utenti_log"

class Type_idSearch(models.Model):
    articleIdCode=models.IntegerField()
    typeOutJson=models.CharField(max_length=4, default="HTML")

class Search_idUser(models.Model):
    journalistId=models.IntegerField()

class Count_words_onItem(models.Model):
    sWord=models.CharField(max_length=26)


