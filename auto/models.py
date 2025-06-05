from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Zakaznik(models.Model):
    jmeno = models.CharField(max_length=45,verbose_name="Jméno zákazníka",help_text="Zadejte křestní jméno",error_messages={'blank': "Jméno autora musí být vyplněno!"})
    prijmeni = models.CharField(max_length=45,verbose_name="Přijmení zakazníka",help_text="Zadejte přijemní",error_messages={'blank':"Přijmení autora musí být vyplněno!"})
    datum_narozeni = models.DateField(blank=True, null=True, verbose_name='Datum narození')
    email = models.CharField(max_length=38,verbose_name="e-mail zákaznika",help_text="Zadejte e-mail")
    telefon = models.CharField(max_length=9)

    class Meta:
        ordering = ['prijmeni', 'jmeno']
        verbose_name = 'Zakazník'
        verbose_name_plural = 'Zákazníci'

    def __str__(self):
        return f"{self.jmeno} {self.prijmeni}"

class Auto(models.Model):
    znacka = models.CharField(max_length=45,verbose_name="Značka auta",help_text="Zadejte značku auta")
    model = models.CharField(max_length=45,verbose_name="Model dané značky auta")
    rok_vyroby = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1900), MaxValueValidator(2025)],verbose_name='Rok vydání', help_text='Zadejte rok vydání (1900 - 2025)')
    dostupnost = models.BooleanField()
    cena_za_den = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Auto"
        verbose_name_plural = "Auta"

    def __str__(self):
        return f"{self.znacka} {self.model}"

class Pujcka(models.Model):
    datum_pujceni = models.DateField()
    datum_vraceni = models.DateField(blank=True, null=True)
    zakaznik = models.ForeignKey(Zakaznik, on_delete=models.CASCADE)
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
    cena = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Pujcka"
        verbose_name_plural = "Pujcky   "

    def __str__(self):
        return f"Půjčka #{self.id} - {self.zakaznik}"

class Platba(models.Model):
    datum_platby = models.DateField(verbose_name="Datum platby")
    castka = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Částka")
    pujcka = models.ForeignKey(Pujcka, on_delete=models.CASCADE, verbose_name="Půjčka")

    class Meta:
        verbose_name = "Platba"
        verbose_name_plural = "Platby"

    def __str__(self):
        return f"Platba #{self.id} - {self.castka} Kč"

class Servis(models.Model):
    datum = models.DateField()
    cena = models.DecimalField(max_digits=12, decimal_places=2)
    popis_servisu = models.TextField(verbose_name="Popis servisu")
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Servis      "
        verbose_name_plural = "Servisy"

    def __str__(self):
        return f"Servis #{self.id} - {self.auto}"
