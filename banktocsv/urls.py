from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'banktocsv'

def redirect_to_home(request):
    """Redirige toutes les anciennes routes vers la page principale"""
    return redirect('banktocsv:index')

urlpatterns = [
    # Page principale avec convertisseur intégré
    path('', views.index, name='index'),
    
    # APIs nécessaires pour le fonctionnement
    path('api/upload/', views.process_upload, name='process_upload'),
    path('api/download/', views.download_direct, name='download_direct'),
    
    # Redirections pour simplifier l'expérience utilisateur
    path('converter/', redirect_to_home, name='converter'),
    path('upload/', redirect_to_home, name='upload'),
    path('statement/<int:statement_id>/', redirect_to_home, name='statement_detail'),
    path('statement/<int:statement_id>/export/', redirect_to_home, name='export_statement'),
    path('statement/<int:statement_id>/download/csv/', redirect_to_home, name='download_csv'),
    path('statement/<int:statement_id>/download/excel/', redirect_to_home, name='download_excel'),
    path('statement/<int:statement_id>/delete/', redirect_to_home, name='delete_statement'),
    path('statement/<int:statement_id>/confirm-delete/', redirect_to_home, name='confirm_delete_statement'),
    path('api/download/<int:statement_id>/<str:format_type>/', redirect_to_home, name='download_file'),
]
