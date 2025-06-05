from django.urls import path
from . import views

urlpatterns = [
 
    path('', views.index, name='index'),
    

    path('auta/', views.seznam_aut, name='seznam_aut'),
    path('auta/<int:pk>/', views.detail_auta, name='detail_auta'),
    path('auta/pridat/', views.pridat_auto, name='pridat_auto'),
    path('auta/<int:pk>/smazat/', views.smazat_auto, name='smazat_auto'),
    

    path('zakaznici/', views.seznam_zakazniku, name='seznam_zakazniku'),
    path('zakaznici/<int:pk>/', views.detail_zakaznika, name='detail_zakaznika'),
    path('zakaznici/pridat/', views.pridat_zakaznika, name='pridat_zakaznika'),
    path('zakaznici/<int:pk>/smazat/', views.smazat_zakaznika, name='smazat_zakaznika'),
    
    path('pujcky/', views.seznam_pujcek, name='seznam_pujcek'),
    path('pujcky/<int:pk>/', views.detail_pujcky, name='detail_pujcky'),
    path('pujcky/pridat/', views.pridat_pujcku, name='pridat_pujcku'),
    path('pujcky/<int:pk>/smazat/', views.smazat_pujcku, name='smazat_pujcku'),
    

    path('platby/', views.seznam_plateb, name='seznam_plateb'),
    path('platby/<int:pk>/', views.detail_platby, name='detail_platby'),
    path('platby/pridat/', views.pridat_platbu, name='pridat_platbu'),
    path('platby/<int:pk>/smazat/', views.smazat_platbu, name='smazat_platbu'),
    

    path('servisy/', views.seznam_servisu, name='seznam_servisu'),
    path('servisy/<int:pk>/', views.detail_servisu, name='detail_servisu'),
    path('servisy/pridat/', views.pridat_servis, name='pridat_servis'),
    path('servisy/<int:pk>/smazat/', views.smazat_servis, name='smazat_servis'),
]
