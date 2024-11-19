from django.urls import path
from . import views

app_name = 'tipos'

urlpatterns = [
    path('<slug:slug>',views.category , name="tipo"),
    path('', views.tipos, name='tipos'),
    path('create/', views.TipoCreateView, name='tipo_create'),
    path('<slug:slug>/delete',views.TipoDeleteView , name="tipo_delete"),
    path('<slug:slug>/edit',views.TipoEditView , name="tipo_edit"),
]