from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Páginas Institucionais & Módulos da SPA
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('automovel/', views.automovel_view, name='automovel'),
    path('alavancas/', views.alavancas_view, name='alavancas'),
    path('layout/', views.layout_view, name='layout'),
    path('analista/', views.analista_view, name='analista'),
    path('industria/', views.industria_view, name='industria'),
    path('gestao/', views.gestao_view, name='gestao'),
    path('cliente/<uuid:token>/', views.portal_cliente_view, name='portal_cliente'),
    path('relatorios/', views.relatorios_lista_view, name='relatorios_lista'),
    path('relatorios/<int:relatorio_id>/', views.relatorio_detalhe_view, name='relatorio_detalhe'),
    path('verificacao/', views.verificacao_view, name='verificacao'),
    path('documentos/', views.documentos_view, name='documentos'),

    # APIs REST / AJAX
    path('api/toggle-pvp/<int:artigo_id>/', views.api_toggle_pvp, name='api_toggle_pvp'),
    path('api/resolver-rutura/<int:rutura_id>/', views.api_resolver_rutura, name='api_resolver_rutura'),
    path('api/corrigir-iva/<int:erro_id>/', views.api_corrigir_iva, name='api_corrigir_iva'),
    path('api/toggle-checklist-item/<int:item_id>/', views.api_toggle_checklist_item, name='api_toggle_checklist_item'),
    path('api/calcular-diagnostico/', views.api_calcular_diagnostico, name='api_calcular_diagnostico'),
    path('api/solicitar-diagnostico/', views.api_solicitar_diagnostico, name='api_solicitar_diagnostico'),
    path('api/toggle-desagio/<int:viatura_id>/', views.api_toggle_desagio, name='api_toggle_desagio'),
    path('api/calcular-diagnostico-auto/', views.api_calcular_diagnostico_auto, name='api_calcular_diagnostico_auto'),
    path('api/toggle-plano-acao/<int:plano_id>/', views.api_toggle_plano_acao, name='api_toggle_plano_acao'),
]
