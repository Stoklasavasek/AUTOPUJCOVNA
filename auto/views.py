from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Zakaznik, Auto, Pujcka, Platba, Servis
from .forms import AutoForm, ZakaznikForm, PujckaForm, PlatbaForm, ServisForm
from django.utils import timezone
from django.db.models import Q


def index(request):
    aktivni_pujcky = Pujcka.objects.filter(
        Q(datum_vraceni__isnull=True) | Q(datum_vraceni__gte=timezone.now().date())
    ).select_related('auto', 'zakaznik').order_by('datum_vraceni')
    
    context = {
        'nadpis': 'Hlavní stránka',
        'pocet_zakazniku': Zakaznik.objects.count(),
        'pocet_aut': Auto.objects.count(),
        'pocet_pujcek': aktivni_pujcky.count(),
        'aktivni_pujcky': aktivni_pujcky
    }
    return render(request, 'index.html', context)


def seznam_aut(request):
    auta = Auto.objects.all()
    
    znacka = request.GET.get('znacka')
    if znacka:
        auta = auta.filter(znacka__icontains=znacka)
    
    model = request.GET.get('model')
    if model:
        auta = auta.filter(model__icontains=model)
    
    dostupnost = request.GET.get('dostupnost')
    if dostupnost:
        auta = auta.filter(dostupnost=dostupnost == '1')
    
    context = {
        'nadpis': 'Seznam aut',
        'auta': auta.order_by('znacka', 'model')
    }
    return render(request, 'auta/auta_seznam.html', context)


def detail_auta(request, pk):
    auto = get_object_or_404(Auto, pk=pk)
    return render(request, 'auta/detail_auta.html', {'auto': auto})


def pridat_auto(request):
    if request.method == 'POST':
        form = AutoForm(request.POST)
        if form.is_valid():
            auto = form.save()
            messages.success(request, f'Auto {auto.znacka} {auto.model} bylo úspěšně přidáno.')
            return redirect('detail_auta', pk=auto.pk)
    else:
        form = AutoForm()
    return render(request, 'auta/pridat_auto.html', {'form': form})


def smazat_auto(request, pk):
    auto = get_object_or_404(Auto, pk=pk)
    if request.method == 'POST':
        if not auto.pujcka_set.exists():
            znacka = auto.znacka
            model = auto.model
            auto.delete()
            messages.success(request, f'Auto {znacka} {model} bylo úspěšně smazáno.')
            return redirect('seznam_aut')
        else:
            messages.error(request, 'Nelze smazat auto s aktivními půjčkami.')
    return redirect('detail_auta', pk=pk)


def seznam_zakazniku(request):
    zakaznici = Zakaznik.objects.all()
    
    jmeno = request.GET.get('jmeno')
    if jmeno:
        zakaznici = zakaznici.filter(jmeno__icontains=jmeno)
    
    prijmeni = request.GET.get('prijmeni')
    if prijmeni:
        zakaznici = zakaznici.filter(prijmeni__icontains=prijmeni)
    
    email = request.GET.get('email')
    if email:
        zakaznici = zakaznici.filter(email__icontains=email)
    
    if request.method == 'POST':
        form = ZakaznikForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zákazník byl úspěšně přidán.')
            return redirect('seznam_zakazniku')
    else:
        form = ZakaznikForm()
    
    context = {
        'nadpis': 'Seznam zákazníků',
        'zakaznici': zakaznici.order_by('prijmeni', 'jmeno'),
        'form': form
    }
    return render(request, 'zakaznici/seznam.html', context)


def detail_zakaznika(request, pk):
    zakaznik = get_object_or_404(Zakaznik, pk=pk)
    aktivni_pujcky = zakaznik.pujcka_set.filter(datum_vraceni__isnull=True).count()
    context = {
        'zakaznik': zakaznik,
        'pujcky': zakaznik.pujcka_set.all(),
        'pocet_aktivnich_pujcek': aktivni_pujcky
    }
    return render(request, 'zakaznici/detail.html', context)


def pridat_zakaznika(request):
    if request.method == 'POST':
        form = ZakaznikForm(request.POST)
        if form.is_valid():
            zakaznik = form.save()
            messages.success(request, f'Zákazník {zakaznik.jmeno} {zakaznik.prijmeni} byl úspěšně přidán.')
            return redirect('detail_zakaznika', pk=zakaznik.pk)
    else:
        form = ZakaznikForm()
    return render(request, 'zakaznici/pridat_zakaznika.html', {'form': form})


def smazat_zakaznika(request, pk):
    zakaznik = get_object_or_404(Zakaznik, pk=pk)
    if request.method == 'POST':
        if not zakaznik.pujcka_set.exists():
            jmeno = zakaznik.jmeno
            prijmeni = zakaznik.prijmeni
            zakaznik.delete()
            messages.success(request, f'Zákazník {jmeno} {prijmeni} byl úspěšně smazán.')
            return redirect('seznam_zakazniku')
        else:
            messages.error(request, 'Nelze smazat zákazníka s aktivními půjčkami.')
    return redirect('detail_zakaznika', pk=pk)


def seznam_pujcek(request):
    pujcky = Pujcka.objects.all()
    
    stav = request.GET.get('stav')
    if stav == 'aktivni':
        pujcky = pujcky.filter(datum_vraceni__isnull=True)
    elif stav == 'vracene':
        pujcky = pujcky.filter(datum_vraceni__isnull=False)
    
    datum_od = request.GET.get('datum_od')
    if datum_od:
        pujcky = pujcky.filter(datum_pujceni__gte=datum_od)
    
    datum_do = request.GET.get('datum_do')
    if datum_do:
        pujcky = pujcky.filter(datum_pujceni__lte=datum_do)
    
    context = {
        'nadpis': 'Seznam půjček',
        'pujcky': pujcky.order_by('-datum_pujceni')
    }
    return render(request, 'pujcky/seznam.html', context)


def detail_pujcky(request, pk):
    pujcka = get_object_or_404(Pujcka, pk=pk)
    return render(request, 'pujcky/detail.html', {'pujcka': pujcka})


def pridat_pujcku(request):
    if request.method == 'POST':
        form = PujckaForm(request.POST)
        if form.is_valid():
            pujcka = form.save()
            messages.success(request, 'Půjčka byla úspěšně přidána.')
            return redirect('detail_pujcky', pk=pujcka.pk)
    else:
        form = PujckaForm()
    return render(request, 'pujcky/pridat_pujcku.html', {'form': form})


def smazat_pujcku(request, pk):
    pujcka = get_object_or_404(Pujcka, pk=pk)
    if request.method == 'POST':
        pujcka.delete()
        messages.success(request, 'Půjčka byla úspěšně smazána.')
        return redirect('seznam_pujcek')
    return redirect('detail_pujcky', pk=pk)


def seznam_plateb(request):
    platby = Platba.objects.all()
    
    datum_od = request.GET.get('datum_od')
    if datum_od:
        platby = platby.filter(datum_platby__gte=datum_od)
    
    datum_do = request.GET.get('datum_do')
    if datum_do:
        platby = platby.filter(datum_platby__lte=datum_do)
    
    context = {
        'nadpis': 'Seznam plateb',
        'platby': platby.order_by('-datum_platby')
    }
    return render(request, 'platby/seznam.html', context)


def detail_platby(request, pk):
    platba = get_object_or_404(Platba, pk=pk)
    return render(request, 'platby/detail.html', {'platba': platba})


def pridat_platbu(request):
    if request.method == 'POST':
        form = PlatbaForm(request.POST)
        if form.is_valid():
            platba = form.save()
            messages.success(request, 'Platba byla úspěšně přidána.')
            return redirect('detail_platby', pk=platba.pk)
    else:
        form = PlatbaForm()
    return render(request, 'platby/pridat_platbu.html', {'form': form})


def smazat_platbu(request, pk):
    platba = get_object_or_404(Platba, pk=pk)
    if request.method == 'POST':
        platba.delete()
        messages.success(request, 'Platba byla úspěšně smazána.')
        return redirect('seznam_plateb')
    return redirect('detail_platby', pk=pk)


def seznam_servisu(request):
    servisy = Servis.objects.all()
    
    datum_od = request.GET.get('datum_od')
    if datum_od:
        servisy = servisy.filter(datum__gte=datum_od)
    
    datum_do = request.GET.get('datum_do')
    if datum_do:
        servisy = servisy.filter(datum__lte=datum_do)
    
    auto = request.GET.get('auto')
    if auto:
        servisy = servisy.filter(auto__id=auto)
    
    context = {
        'nadpis': 'Seznam servisů',
        'servisy': servisy.order_by('-datum'),
        'auta': Auto.objects.all().order_by('znacka', 'model')
    }
    return render(request, 'servisy/seznam.html', context)


def detail_servisu(request, pk):
    servis = get_object_or_404(Servis, pk=pk)
    return render(request, 'servisy/detail.html', {'servis': servis})


def pridat_servis(request):
    if request.method == 'POST':
        form = ServisForm(request.POST)
        if form.is_valid():
            servis = form.save()
            messages.success(request, 'Servis byl úspěšně přidán.')
            return redirect('detail_servisu', pk=servis.pk)
    else:
        form = ServisForm()
    return render(request, 'servisy/pridat_servis.html', {'form': form})


def smazat_servis(request, pk):
    servis = get_object_or_404(Servis, pk=pk)
    if request.method == 'POST':
        servis.delete()
        messages.success(request, 'Servis byl úspěšně smazán.')
        return redirect('seznam_servisu')
    return redirect('detail_servisu', pk=pk)
