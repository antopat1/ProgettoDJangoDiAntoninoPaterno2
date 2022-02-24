from django import forms
from django.core.exceptions import ValidationError #i validatori approfonditi sulla doc ufficiali permettono di validare i dati solo a determinate condizioni
from .models import News,Type_idSearch,Search_idUser,Count_words_onItem
from django.contrib.auth.models import User

class FormRegistrazionUser(forms.ModelForm):

    username=forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.EmailInput())
    password=forms.CharField(widget=forms.PasswordInput())
    conferma_password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ["username","email","password","conferma_password"]

    def clean(self):   #metodo per validare i dati, nello specifico le due password coincidenti
        super().clean()
        password= self.cleaned_data["password"]
        password_confirm = self.cleaned_data["conferma_password"]
        if password!=password_confirm:
            raise forms.ValidationError("Le password non combaciano")
        return self.cleaned_data



class WriteNewsModelForm(forms.ModelForm):

    contenuto = forms.CharField(required=False,widget=forms.TextInput( attrs = {
            'hidden': '',
        }))   #un campo che non voglio visualizzare ma che mi aiuta nella validazione

    class Meta():
        model= News
        fields= "__all__"
        exclude = ["user","hash","txId"]

    def clean_contenuto(self):
        super().clean()
        self.cleaned_data["contenuto"]=self.cleaned_data['content']
        data = self.cleaned_data["contenuto"]

        if "hack" in data:
            raise ValidationError("Attenzione il post inserito contiene la parola 'hack' pertanto viola le norme del sito!")

        self.contenuto=self.cleaned_data["content"]
        print(self.contenuto)

        return data


class ChoiceForm(forms.ModelForm):
    class Meta():
        model= Type_idSearch
        fields= "__all__"

class FormJournalist(forms.ModelForm):
    class Meta():
        model= Search_idUser
        fields= "__all__"

class FormCountwords(forms.ModelForm):
    class Meta():
        model= Count_words_onItem
        fields= "__all__"
