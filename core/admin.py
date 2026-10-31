from django.contrib import admin
from .models import (
    Supermercado, LeadDiagnostico, ArtigoCurvaA, RuturaFantasma, StockMorto,
    ErroIvaSaft, AlertaMobile, RelatorioAuditoria, AreaVerificacao, ChecklistItem, DocumentoConsultoria,
    EmpresaAutomovel, ViaturaStand, OrdemOficina, SegmentoRentACar, AlertaAutomovel,
    AlavancaVenda, PlanoAcaoOperacional, LayoutSupermercadoItem, RedeSetorialRanking,
    PortalClienteToken, OportunidadeIndustria
)

@admin.register(Supermercado)
class SupermercadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nif', 'localizacao', 'software_pos', 'faturacao_mensal', 'margem_teorica', 'margem_real')
    search_fields = ('nome', 'nif', 'razao_social')

@admin.register(LeadDiagnostico)
class LeadDiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'empresa', 'email', 'telemovel', 'distrito', 'lojas', 'faturacao', 'status', 'criado_em')
    list_filter = ('status', 'distrito', 'lojas')
    search_fields = ('nome', 'empresa', 'email', 'telemovel', 'nif')
    readonly_fields = ('criado_em',)

@admin.register(ArtigoCurvaA)
class ArtigoCurvaAAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'artigo', 'familia', 'custo_medio_pos', 'custo_ultima_fatura', 'pvp_atual', 'pvp_sugerido', 'perda_mensal', 'atualizado')
    list_filter = ('atualizado', 'familia', 'iva')
    search_fields = ('codigo', 'ean', 'artigo', 'fornecedor')

@admin.register(RuturaFantasma)
class RuturaFantasmaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'artigo', 'stock_sistema', 'horas_sem_venda', 'perda_estimada_mes', 'resolvido')
    list_filter = ('resolvido',)
    search_fields = ('codigo', 'artigo', 'causa_provavel')

@admin.register(StockMorto)
class StockMortoAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'skus', 'dias_sem_venda', 'capital_imobilizado', 'sugestao')
    search_fields = ('categoria',)

@admin.register(ErroIvaSaft)
class ErroIvaSaftAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao', 'iva_compra', 'iva_venda_pos', 'prejuizo_mensal', 'corrigido')
    list_filter = ('corrigido',)
    search_fields = ('codigo', 'descricao')

@admin.register(AlertaMobile)
class AlertaMobileAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'canal', 'hora', 'ecra_destino', 'lido')
    list_filter = ('lido', 'canal')
    search_fields = ('tipo', 'mensagem')

@admin.register(RelatorioAuditoria)
class RelatorioAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('codigo_doc', 'titulo', 'tipo', 'periodo', 'valor_impacto', 'criado_em')
    list_filter = ('tipo', 'periodo')
    search_fields = ('codigo_doc', 'titulo', 'resumo_executivo')

class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItem
    extra = 1

@admin.register(AreaVerificacao)
class AreaVerificacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'responsavel_padrao', 'ordem')
    inlines = [ChecklistItemInline]

@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('area', 'ponto_verificacao', 'status', 'frequencia', 'risco_financeiro')
    list_filter = ('status', 'area', 'frequencia')
    search_fields = ('ponto_verificacao', 'procedimento_padrao')

@admin.register(DocumentoConsultoria)
class DocumentoConsultoriaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'titulo', 'categoria', 'formato', 'enquadramento_legal')
    list_filter = ('categoria', 'formato')
    search_fields = ('codigo', 'titulo', 'descricao')

# Modelos do Módulo Automóvel 360º
@admin.register(EmpresaAutomovel)
class EmpresaAutomovelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nif', 'localizacao', 'segmento_principal', 'faturacao_mensal')
    search_fields = ('nome', 'nif', 'localizacao')
    list_filter = ('segmento_principal',)

@admin.register(ViaturaStand)
class ViaturaStandAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'modelo', 'tipo', 'dias_em_stock', 'custo_aquisicao', 'pvp_tabela', 'floor_plan_acumulado')
    search_fields = ('matricula', 'modelo')
    list_filter = ('tipo',)

@admin.register(OrdemOficina)
class OrdemOficinaAdmin(admin.ModelAdmin):
    list_display = ('numero_or', 'viatura', 'tecnico', 'horas_faturadas', 'taxa_ocupacao_percentual', 'margem_pecas_percentual', 'status')
    search_fields = ('numero_or', 'viatura', 'tecnico')
    list_filter = ('status',)

@admin.register(SegmentoRentACar)
class SegmentoRentACarAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'tamanho_frota', 'taxa_ocupacao_media', 'tarifa_media_diaria', 'revpav_real')

@admin.register(AlertaAutomovel)
class AlertaAutomovelAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'pilar', 'severidade', 'lido', 'data_alerta')
    list_filter = ('pilar', 'severidade', 'lido')

# Modelos do Ecossistema Novo Varejo (Slide 87)
@admin.register(AlavancaVenda)
class AlavancaVendaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor_atual', 'meta_otimizada', 'unidade', 'impacto_previsto_euros')

@admin.register(PlanoAcaoOperacional)
class PlanoAcaoOperacionalAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'responsavel', 'prazo_dias', 'status', 'ganho_estimado_mensal')
    list_filter = ('status',)

@admin.register(LayoutSupermercadoItem)
class LayoutSupermercadoItemAdmin(admin.ModelAdmin):
    list_display = ('zona', 'tipo_circulacao', 'indice_frio_calor', 'impacto_venda_m2')

@admin.register(RedeSetorialRanking)
class RedeSetorialRankingAdmin(admin.ModelAdmin):
    list_display = ('posicao', 'insignia', 'quota_mercado_pct', 'faturacao_estimada_milhoes')

@admin.register(OportunidadeIndustria)
class OportunidadeIndustriaAdmin(admin.ModelAdmin):
    list_display = ('produto', 'rede_retalho', 'taxa_rutura_linear_pct', 'potencial_sellout_adicional_mes')

@admin.register(PortalClienteToken)
class PortalClienteTokenAdmin(admin.ModelAdmin):
    list_display = ('supermercado', 'token', 'ativo', 'criado_em')
