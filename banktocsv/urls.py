from django.urls import path
from . import views

app_name = 'banktocsv'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_statement, name='upload'),
    path('statement/<int:statement_id>/', views.statement_detail, name='statement_detail'),
    path('statement/<int:statement_id>/export/', views.export_statement, name='export_statement'),
    path('statement/<int:statement_id>/download/csv/', views.download_csv, name='download_csv'),
    path('statement/<int:statement_id>/download/excel/', views.download_excel, name='download_excel'),
    path('statement/<int:statement_id>/delete/', views.delete_statement, name='delete_statement'),
    path('statement/<int:statement_id>/confirm-delete/', views.confirm_delete_statement, name='confirm_delete_statement'),
]
