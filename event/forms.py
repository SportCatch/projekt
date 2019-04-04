from django import forms
import re
from django.utils.safestring import mark_safe
from .models import *




class wydarzenieForm(forms.ModelForm):
    class Meta:
        model = wydarzenie
        fields = ('nazwa', 'opis', 'miejsce', 'data_rozpoczecia','photo')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['miejsce'].queryset = miejsce.objects.filter(zaakceptowane=True).order_by('nazwa')



class WydarzenieForm(forms.ModelForm):
    class Meta:
        model=wydarzenie
        fields = ('nazwa', 'opis', 'miejsce', 'data_rozpoczecia', 'photo')

    def clean_data_rozpoczecia(self, *args,**kwargs):
        data_rozpoczecia = self.cleaned_data.get("data_rozpoczecia")
        data = str(data_rozpoczecia)
        print(data)
        if re.fullmatch('^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$', data) is None:
            raise forms.ValidationError("Podaj datę w formacie YYYY-MM-DD")
        return data_rozpoczecia

        
class ogloszenieForm(forms.ModelForm):
	class Meta:
		model = ogloszenie
		fields = ('tytul','opis', 'zdjecie')
        
class komentarzWydarzeniaForm(forms.ModelForm):
    class Meta:
        model=komentarz_do_wydarzenia
        fields=['tresc',]
class komentarzeMiejscaForm(forms.ModelForm):
    class Meta:
        model=komentarz_do_miejsca
        fields=['tresc',]
class miejsceForm(forms.ModelForm):
    class Meta:
        model = miejsce
        fields = ('adres', 'miasto', 'nazwa', 'photo')

    
    def clean_miasto(self, *args,**kwargs):
        miasto = self.cleaned_data.get("miasto")
        p = re.compile('[^0-9]*')
        if p.fullmatch(miasto) is None:
            raise forms.ValidationError("Nazwa miasta nie powinna zawierać cyfr")
        elif re.fullmatch('[^@?#$%&^-]*',miasto) is None:
             raise forms.ValidationError("Nazwa miasta nie powinna zawierać znaków alfanumerycznych")
        elif len(miasto) < 2:
            raise forms.ValidationError("Nazwa miasta powinna być dłuższa niż 1")
        return miasto
        
    def clean_adres(self, *args,**kwargs):
        adres = self.cleaned_data.get("adres")
        if len(adres) < 2:
            raise forms.ValidationError("Adres powinien być dłuższy niż 1")
        elif re.fullmatch('[^@?#$%&^]*',adres) is None:
            raise forms.ValidationError("Adres nie powinien zawierać znaków alfanumerycznych")
        return adres

class komentarzOgloszenieForm(forms.ModelForm):
    class Meta:
        model= komentarz_do_ogloszenia
        fields= ['tresc',]

class miejsceEditForm(forms.ModelForm):
    class Meta:
        model = miejsce
        fields = ('adres','miasto','nazwa','zaakceptowane')
    
    def clean_miasto(self, *args,**kwargs):
        miasto = self.cleaned_data.get("miasto")
        p = re.compile('[^0-9]*')
        if p.fullmatch(miasto) is None:
            raise forms.ValidationError("Nazwa miasta nie powinna zawierać cyfr")
        elif re.fullmatch('[^@?#$%&^-]*',miasto) is None:
             raise forms.ValidationError("Nazwa miasta nie powinna zawierać znaków alfanumerycznych")
        elif len(miasto) < 2:
            raise forms.ValidationError("Nazwa miasta powinna być dłuższa niż 1")
        return miasto
        
    def clean_adres(self, *args,**kwargs):
        adres = self.cleaned_data.get("adres")
        if len(adres) < 2:
            raise forms.ValidationError("Adres powinien być dłuższy niż 1")
        elif re.fullmatch('[^@?#$%&^]*',adres) is None:
            raise forms.ValidationError("Adres nie powinien zawierać znaków alfanumerycznych")
        return adres

class CommentEditForm(forms.ModelForm):
    class Meta:
        model = komentarz_do_miejsca
        fields = ['tresc',]

class CzatForm(forms.Form):
    def __init__(self, user_r, *args, **kwargs):
        super(CzatForm, self).__init__(*args, **kwargs)
        profile = Profile.objects.get(user=user_r)
        self.fields['choices'] = forms.ModelMultipleChoiceField(
            queryset=profile.friends.all(),
            widget=forms.CheckboxSelectMultiple(),
            label="Zaproś znajomych do rozmowy")

class WiadomoscForm(forms.ModelForm):
    class Meta:
        model = Wiadomosc
        fields = ('tresc',)
        labels = {"tresc": ""}
    
