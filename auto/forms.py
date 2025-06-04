from django import forms
from .models import Auto, Zakaznik, Pujcka, Platba, Servis

class AutoForm(forms.ModelForm):
    class Meta:
        model = Auto
        fields = ['znacka', 'model', 'rok_vyroby', 'dostupnost', 'cena_za_den']
        widgets = {
            'znacka': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Např. Škoda'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Např. Octavia'}),
            'rok_vyroby': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Např. 2020'}),
            'dostupnost': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cena_za_den': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Kč/den'})
        }

class ZakaznikForm(forms.ModelForm):
    class Meta:
        model = Zakaznik
        fields = ['jmeno', 'prijmeni', 'datum_narozeni', 'email', 'telefon']
        widgets = {
            'jmeno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte jméno'}),
            'prijmeni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zadejte příjmení'}),
            'datum_narozeni': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'telefon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123456789'})
        }

class PujckaForm(forms.ModelForm):
    datum_vraceni = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Datum vrácení (volitelné)'
    )

    class Meta:
        model = Pujcka
        fields = ['datum_pujceni', 'datum_vraceni', 'zakaznik', 'auto', 'cena']
        widgets = {
            'datum_pujceni': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'zakaznik': forms.Select(attrs={'class': 'form-select'}),
            'auto': forms.Select(attrs={'class': 'form-select'}),
            'cena': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Celková cena'})
        }

class PlatbaForm(forms.ModelForm):
    class Meta:
        model = Platba
        fields = ['datum_platby', 'castka', 'pujcka']
        widgets = {
            'datum_platby': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'castka': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Částka v Kč'}),
            'pujcka': forms.Select(attrs={'class': 'form-select'})
        }

class ServisForm(forms.ModelForm):
    class Meta:
        model = Servis
        fields = ['datum', 'cena', 'popis_servisu', 'auto']
        widgets = {
            'datum': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cena': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cena servisu v Kč'}),
            'popis_servisu': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Popis provedených prací'}),
            'auto': forms.Select(attrs={'class': 'form-select'})
        } 