import uuid
from django.db import models
from django.utils import timezone

class Supermercado(models.Model):
    nome = models.CharField('Nome Comercial', max_length=200)
    razao_social = models.CharField('Firma / Razão Social', max_length=250)
    nif = models.CharField('NIF / NIPC', max_length=20, unique=True)
    localizacao = models.CharField('Concelho / Região', max_length=150)
    area_m2 = models.IntegerField('Área de Venda (m²)', default=400)
    num_caixas = models.IntegerField('N.º de Linhas de Caixa (POS)', default=3)
    num_colaboradores = models.IntegerField('N.º de Colaboradores', default=14)
    software_pos = models.CharField('Software POS / ERP', max_length=100, default='ETPOS')
    faturacao_mensal = models.DecimalField('Faturação Mensal s/ IVA (€)', max_digits=12, decimal_places=2, default=120000.00)
    margem_teorica = models.DecimalField('Margem de Sistema (%)', max_digits=5, decimal_places=2, default=24.50)
    margem_real = models.DecimalField('Margem Real Auditada (%)', max_digits=5, decimal_places=2, default=19.50)

    class Meta:
        verbose_name = 'Supermercado Cliente'
        verbose_name_plural = 'Supermercados Clientes'

    def __str__(self):
        return f"{self.nome} ({self.localizacao})"


class LeadDiagnostico(models.Model):
    STATUS_CHOICES = [
        ('novo', 'Novo Pedido'),
        ('em_analise', 'Em Análise de SAF-T'),
        ('reuniao_agendada', 'Raio-X Agendado'),
        ('proposta_enviada', 'Proposta de Avença Enviada'),
        ('ativo', 'Cliente em Avença'),
    ]

    nome = models.CharField('Nome do Sócio-Gerente / Diretor', max_length=150)
    empresa = models.CharField('Supermercado / Grupo Retalhista', max_length=200)
    nif = models.CharField('NIF da Empresa', max_length=20, blank=True, null=True)
    email = models.EmailField('Correio Eletrónico')
    telemovel = models.CharField('Telemóvel / WhatsApp', max_length=30)
    distrito = models.CharField('Distrito / Região', max_length=100, default='Lisboa e Vale do Tejo')
    lojas = models.CharField('N.º de Lojas no Grupo', max_length=50, default='1 a 3 lojas')
    faturacao = models.CharField('Faturação Mensal Global', max_length=60, default='100.000 € a 250.000 €')
    software_pos = models.CharField('Software de Faturação / POS', max_length=80, blank=True, null=True)
    mensagem = models.TextField('Principais Dores Operacionais', blank=True, null=True)
    status = models.CharField('Estado do Processo', max_length=30, choices=STATUS_CHOICES, default='novo')
    criado_em = models.DateTimeField('Data do Pedido', default=timezone.now)

    class Meta:
        verbose_name = 'Pedido de Diagnóstico Raio-X'
        verbose_name_plural = 'Pedidos de Diagnóstico Raio-X'
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.nome} - {self.empresa} ({self.distrito})"


class ArtigoCurvaA(models.Model):
    codigo = models.CharField('Código do Artigo', max_length=20, unique=True)
    ean = models.CharField('Código de Barras (EAN-13)', max_length=30)
    artigo = models.CharField('Designação do Artigo', max_length=255)
    familia = models.CharField('Família / Categoria', max_length=100)
    custo_medio_pos = models.DecimalField('Custo Médio no Sistema POS (€)', max_digits=8, decimal_places=2)
    custo_ultima_fatura = models.DecimalField('Custo Última Fatura no Cais (€)', max_digits=8, decimal_places=2)
    pvp_atual = models.DecimalField('PVP Atual na Prateleira (€)', max_digits=8, decimal_places=2)
    pvp_sugerido = models.DecimalField('PVP Sugerido de Blindagem (€)', max_digits=8, decimal_places=2)
    iva = models.IntegerField('Taxa de IVA Legal (%)', default=6)
    volume_mensal = models.IntegerField('Vendas Médias Mensais (Un.)', default=100)
    perda_mensal = models.DecimalField('Perda Mensal por Erosão (€)', max_digits=8, decimal_places=2)
    atualizado = models.BooleanField('PVP Atualizado no POS', default=False)
    fornecedor = models.CharField('Fornecedor / Grossista MARL', max_length=150)

    class Meta:
        verbose_name = 'Artigo Curva A (Erosão de Preço)'
        verbose_name_plural = 'Artigos Curva A (Erosão de Preço)'
        ordering = ['-perda_mensal']

    def __str__(self):
        return f"{self.codigo} - {self.artigo}"


class RuturaFantasma(models.Model):
    codigo = models.CharField('Código do Artigo', max_length=20, unique=True)
    artigo = models.CharField('Designação do Artigo', max_length=255)
    stock_sistema = models.IntegerField('Stock Informático no POS')
    horas_sem_venda = models.CharField('Horas Decorridas sem Leituras na Caixa', max_length=80)
    causa_provavel = models.CharField('Diagnóstico Técnico da Causa', max_length=255)
    perda_estimada_mes = models.DecimalField('Perda Mensal Estimada (€)', max_digits=8, decimal_places=2)
    resolvido = models.BooleanField('Reposição Validada no Linear', default=False)

    class Meta:
        verbose_name = 'Rutura Fantasma (Stock Virtual)'
        verbose_name_plural = 'Ruturas Fantasma (Stock Virtual)'

    def __str__(self):
        return f"{self.artigo} ({self.stock_sistema} un.)"


class StockMorto(models.Model):
    categoria = models.CharField('Secção / Categoria de Produto', max_length=150)
    skus = models.IntegerField('N.º de Referências Afetadas')
    dias_sem_venda = models.CharField('Tempo sem Movimentação', max_length=50)
    capital_imobilizado = models.DecimalField('Capital Imobilizado (€)', max_digits=10, decimal_places=2)
    sugestao = models.CharField('Medida de Escoamento e Liquidação', max_length=255)

    class Meta:
        verbose_name = 'Stock Morto (Curva C)'
        verbose_name_plural = 'Stock Morto (Curva C)'

    def __str__(self):
        return f"{self.categoria} (€ {self.capital_imobilizado})"


class ErroIvaSaft(models.Model):
    codigo = models.CharField('Código do Artigo', max_length=30, unique=True)
    descricao = models.CharField('Designação do Artigo', max_length=255)
    iva_compra = models.CharField('Taxa IVA na Compra (Fatura Cais)', max_length=10)
    iva_venda_pos = models.CharField('Taxa IVA no POS (Venda Cliente)', max_length=20)
    diferenca = models.CharField('Divergência Fiscal', max_length=10)
    prejuizo_mensal = models.DecimalField('Prejuízo Fiscal / Margem (€/mês)', max_digits=8, decimal_places=2)
    corrigido = models.BooleanField('Parametrização Corrigida no POS', default=False)

    class Meta:
        verbose_name = 'Divergência Fiscal SAF-T (PT)'
        verbose_name_plural = 'Divergências Fiscais SAF-T (PT)'

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class AlertaMobile(models.Model):
    tipo = models.CharField('Tipologia do Alerta', max_length=120)
    hora = models.CharField('Horário da Deteção', max_length=50)
    canal = models.CharField('Canal de Transmissão (WhatsApp/App)', max_length=100)
    mensagem = models.TextField('Texto do Alerta Técnico')
    ecra_destino = models.CharField('Ecrã de Resolução Direta', max_length=30)
    lido = models.BooleanField('Lido pelo Responsável', default=False)

    class Meta:
        verbose_name = 'Alerta Mobile (WhatsApp Retalho)'
        verbose_name_plural = 'Alertas Mobile (WhatsApp Retalho)'

    def __str__(self):
        return f"{self.tipo} - {self.canal}"


# ==========================================
# NOVOS MÓDULOS DE CONSULTORIA DE REFERÊNCIA
# ==========================================

class RelatorioAuditoria(models.Model):
    TIPO_CHOICES = [
        ('cmvc', 'Relatório Mensal de CMVC e Margem Real'),
        ('auto_quebras', 'Auto Oficial de Abate de Quebras (Art.º 86.º CIVA)'),
        ('saf_t', 'Auditoria Fiscal de Parametrização SAF-T (PT)'),
        ('cais', 'Auditoria de Cais de Receção e Conferência Cega'),
        ('talho', 'Balanço de Desmanche e Quebras no Talho'),
        ('equipa', 'Auditoria de Produtividade Laboral e Escalas'),
    ]

    supermercado = models.ForeignKey(Supermercado, on_delete=models.CASCADE, related_name='relatorios', null=True, blank=True)
    tipo = models.CharField('Tipo de Relatório', max_length=30, choices=TIPO_CHOICES)
    titulo = models.CharField('Título do Dossiê', max_length=255)
    periodo = models.CharField('Período de Referência', max_length=80, default='Outubro 2026')
    codigo_doc = models.CharField('Código Documental Formal', max_length=40, unique=True)
    resumo_executivo = models.TextField('Resumo Executivo para a Gerência')
    valor_impacto = models.DecimalField('Impacto Financeiro Auditado (€)', max_digits=12, decimal_places=2)
    parecer_consultor = models.TextField('Parecer e Plano de Ação Recomendado')
    destinatario = models.CharField('Destinatário Principal', max_length=150, default='Sócio-Gerente & Contabilista Certificado (CC)')
    assinado_por = models.CharField('Consultor Responsável', max_length=120, default='Vértice Retalho Portugal • Dr. Carlos Ramos, ROC/CC')
    criado_em = models.DateTimeField('Data de Emissão', default=timezone.now)

    class Meta:
        verbose_name = 'Relatório de Auditoria'
        verbose_name_plural = 'Relatórios de Auditoria'
        ordering = ['-criado_em']

    def __str__(self):
        return f"[{self.codigo_doc}] {self.titulo}"


class AreaVerificacao(models.Model):
    nome = models.CharField('Área / Secção da Loja', max_length=100)
    icone = models.CharField('Ícone Lucide', max_length=50, default='check-square')
    responsavel_padrao = models.CharField('Responsável Operacional', max_length=120)
    descricao = models.TextField('Objetivo do Controlo Diário')
    ordem = models.IntegerField('Ordem de Apresentação', default=1)

    class Meta:
        verbose_name = 'Área de Verificação Operacional'
        verbose_name_plural = 'Áreas de Verificação Operacional'
        ordering = ['ordem']

    def __str__(self):
        return self.nome


class ChecklistItem(models.Model):
    STATUS_CHOICES = [
        ('conforme', 'Conforme ✓'),
        ('nao_conforme', 'Não Conforme ✗'),
        ('em_correcao', 'Em Correção ⚠'),
    ]

    area = models.ForeignKey(AreaVerificacao, on_delete=models.CASCADE, related_name='itens')
    ponto_verificacao = models.CharField('Ponto de Controlo Técnico', max_length=255)
    procedimento_padrao = models.TextField('Procedimento Operacional Padronizado (POP)')
    risco_financeiro = models.CharField('Risco se Não Cumprido', max_length=200)
    status = models.CharField('Estado da Verificação', max_length=20, choices=STATUS_CHOICES, default='conforme')
    frequencia = models.CharField('Frequência de Aferição', max_length=50, default='Diária (Abertura)')
    observacao = models.CharField('Nota do Consultor / Chefe de Loja', max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Item de Checklist de Chão de Loja'
        verbose_name_plural = 'Itens de Checklist de Chão de Loja'

    def __str__(self):
        return f"[{self.area.nome}] {self.ponto_verificacao}"


class DocumentoConsultoria(models.Model):
    CATEGORIA_CHOICES = [
        ('minutas', 'Minutas Formais & Autos Legais (AT/CC)'),
        ('fichas_tecnicas', 'Fichas Técnicas de Rendimento & Frescos'),
        ('pops', 'Procedimentos Operacionais Padronizados (POPs)'),
        ('escalas', 'Matrizes de Escalas & Produtividade Laboral'),
    ]

    categoria = models.CharField('Categoria Documental', max_length=30, choices=CATEGORIA_CHOICES)
    titulo = models.CharField('Nome do Documento / Minuta', max_length=255)
    codigo = models.CharField('Código Normativo', max_length=40, unique=True)
    descricao = models.TextField('Finalidade e Aplicação Prática no Supermercado')
    formato = models.CharField('Formato de Emissão', max_length=20, default='PDF / Word / Excel')
    enquadramento_legal = models.CharField('Enquadramento Legal (PT)', max_length=255, default='Art.º 86.º Código do IVA / SAF-T (PT)')
    conteudo_minuta = models.TextField('Texto / Minuta Integral do Documento')

    class Meta:
        verbose_name = 'Documento / Minuta de Consultoria'
        verbose_name_plural = 'Documentos & Minutas de Consultoria'

    def __str__(self):
        return f"[{self.codigo}] {self.titulo}"


# ==============================================================================
# MODELOS DE CONSULTORIA & BI AUTOMÓVEL (STAND + OFICINA + RENT-A-CAR)
# ==============================================================================

class EmpresaAutomovel(models.Model):
    nome = models.CharField('Nome da Concessão / Empresa', max_length=200, default='AutoVila Motors & Rent Lda.')
    razao_social = models.CharField('Firma / Razão Social', max_length=250, default='AutoVila Comércio, Manutenção e Aluguer de Veículos Lda.')
    nif = models.CharField('NIF / NIPC', max_length=20, unique=True, default='509881223')
    localizacao = models.CharField('Concelho / Região', max_length=150, default='Leiria (Zona Industrial Sul)')
    num_viaturas_frota = models.IntegerField('N.º Viaturas Rent-a-Car', default=48)
    num_elevadores_oficina = models.IntegerField('N.º Postos de Trabalho Oficina', default=6)
    num_carros_stand = models.IntegerField('Viaturas em Stock no Stand', default=35)
    
    faturacao_mensal_global = models.DecimalField('Faturação Global s/ IVA (€)', max_digits=12, decimal_places=2, default=380000.00)
    faturacao_stand = models.DecimalField('Faturação Stand (€)', max_digits=12, decimal_places=2, default=220000.00)
    faturacao_oficina = models.DecimalField('Faturação Oficina (€)', max_digits=12, decimal_places=2, default=95000.00)
    faturacao_rentacar = models.DecimalField('Faturação Rent-a-Car (€)', max_digits=12, decimal_places=2, default=65000.00)
    fuga_mensal_mapeada = models.DecimalField('Fuga Mensal Total (€)', max_digits=12, decimal_places=2, default=14800.00)

    class Meta:
        verbose_name = 'Concessão Automóvel Cliente'
        verbose_name_plural = 'Concessões Automóveis Clientes'

    def __str__(self):
        return f"{self.nome} ({self.localizacao})"


class ViaturaStand(models.Model):
    matricula = models.CharField('Matrícula', max_length=20)
    viatura = models.CharField('Marca, Modelo & Versão', max_length=255)
    ano = models.IntegerField('Ano de Matrícula', default=2021)
    kms = models.IntegerField('Quilometragem (km)', default=65000)
    dias_em_stock = models.IntegerField('Dias em Stock (Aging)', default=45)
    custo_aquisicao = models.DecimalField('Custo de Aquisição / Retoma (€)', max_digits=10, decimal_places=2)
    custo_recondicionamento = models.DecimalField('Custo Preparação & Oficina (€)', max_digits=10, decimal_places=2, default=650.00)
    custo_financeiro_parado = models.DecimalField('Custo Floor Plan Acumulado (€)', max_digits=10, decimal_places=2, default=350.00)
    pvp_anunciado = models.DecimalField('PVP Anunciado (€)', max_digits=10, decimal_places=2)
    pvp_desagio_sugerido = models.DecimalField('PVP Deságio p/ Liquidez (€)', max_digits=10, decimal_places=2)
    regime_iva = models.CharField('Regime de IVA', max_length=80, default='Regime da Margem (DL 199/96)')
    desagio_aplicado = models.BooleanField('Deságio de Liquidez Ativo', default=False)
    status = models.CharField('Estado da Viatura', max_length=30, default='disponivel')

    class Meta:
        verbose_name = 'Viatura em Stock (Stand)'
        verbose_name_plural = 'Viaturas em Stock (Stand)'
        ordering = ['-dias_em_stock']

    def __str__(self):
        return f"{self.viatura} [{self.matricula}] - {self.dias_em_stock} dias"


class OrdemOficina(models.Model):
    numero_or = models.CharField('N.º Ordem de Reparação', max_length=30, unique=True)
    cliente = models.CharField('Cliente / Frota', max_length=150)
    viatura = models.CharField('Viatura Assistida', max_length=200)
    tipo_servico = models.CharField('Tipo de Intervenção', max_length=100, default='Revisão Periódica')
    horas_orcamentadas = models.DecimalField('Horas Orçamentadas', max_digits=5, decimal_places=2, default=3.0)
    horas_faturadas = models.DecimalField('Horas Faturadas no SAF-T', max_digits=5, decimal_places=2, default=2.2)
    valor_mao_obra = models.DecimalField('Valor Mão de Obra (€)', max_digits=8, decimal_places=2, default=99.00)
    custo_pecas_grossista = models.DecimalField('Custo Peças Grossista (€)', max_digits=8, decimal_places=2, default=180.00)
    pvp_pecas_faturado = models.DecimalField('PVP Peças Faturado (€)', max_digits=8, decimal_places=2, default=235.00)
    perda_margem_pecas = models.DecimalField('Perda Margem Peças (€)', max_digits=8, decimal_places=2, default=42.00)

    class Meta:
        verbose_name = 'Ordem de Reparação (Oficina)'
        verbose_name_plural = 'Ordens de Reparação (Oficina)'

    def __str__(self):
        return f"{self.numero_or} - {self.cliente}"


class SegmentoRentACar(models.Model):
    categoria = models.CharField('Grupo / Segmento', max_length=150)
    viaturas_exemplo = models.CharField('Modelos Representativos', max_length=200)
    qtd_viaturas = models.IntegerField('N.º de Carros na Frota', default=12)
    taxa_ocupacao_atual = models.DecimalField('Taxa de Ocupação Atual (%)', max_digits=5, decimal_places=2, default=68.0)
    taxa_ocupacao_alvo = models.DecimalField('Taxa de Ocupação Meta (%)', max_digits=5, decimal_places=2, default=82.0)
    diaria_media = models.DecimalField('Diária Média Cobrada (€)', max_digits=8, decimal_places=2, default=45.00)
    revpav_atual = models.DecimalField('RevPAV Atual (€/dia)', max_digits=8, decimal_places=2, default=30.60)
    revpav_alvo = models.DecimalField('RevPAV Meta (€/dia)', max_digits=8, decimal_places=2, default=36.90)
    custo_km = models.DecimalField('Custo TCO por Km (€)', max_digits=6, decimal_places=3, default=0.135)
    dias_para_desmobilizacao = models.IntegerField('Dias até Desmobilização', default=90)
    tributacao_autonoma = models.CharField('Taxa Tributação Autónoma IRC', max_length=100, default='10% (< 27.500 €)')

    class Meta:
        verbose_name = 'Segmento de Frota Rent-a-Car'
        verbose_name_plural = 'Segmentos de Frota Rent-a-Car'

    def __str__(self):
        return f"{self.categoria} ({self.qtd_viaturas} un.)"


class AlertaAutomovel(models.Model):
    SETOR_CHOICES = [
        ('stand', 'Stand de Vendas (Aging / Margem)'),
        ('oficina', 'Oficina & Peças (Horas / PVP)'),
        ('rentacar', 'Rent-a-Car (Ocupação / TCO)'),
        ('fiscal', 'Fiscal & Tributação Autónoma (IRC/IVA)'),
    ]

    setor = models.CharField('Polo do Negócio', max_length=30, choices=SETOR_CHOICES)
    titulo = models.CharField('Título do Alerta', max_length=200)
    descricao = models.TextField('Descrição Operacional e Solução')
    impacto_euros = models.DecimalField('Impacto Mensal (€)', max_digits=8, decimal_places=2)
    criticidade = models.CharField('Nível de Urgência', max_length=20, default='alta')
    resolvido = models.BooleanField('Resolvido', default=False)
    criado_em = models.DateTimeField('Data do Alerta', default=timezone.now)

    class Meta:
        verbose_name = 'Alerta de Gestão Automóvel'
        verbose_name_plural = 'Alertas de Gestão Automóvel'
        ordering = ['-impacto_euros']

    def __str__(self):
        return f"[{self.get_setor_display()}] {self.titulo}"


# ==============================================================================
# PILARES DO ECOSSISTEMA NOVO VAREJO (METODOLOGIA COMPLETA DE SLIDES & INTELIGÊNCIA)
# ==============================================================================

class AlavancaVenda(models.Model):
    """
    Metodologia: A Fórmula da Venda
    Venda = Clientes (Fluxo) × Ticket Médio
    Ticket Médio = Itens por Cupom/Talão × Valor Médio do Item
    """
    ALAVANCA_CHOICES = [
        ('fluxo', 'Fluxo de Clientes (Visitas/Talões)'),
        ('itens_cupom', 'Itens por Talão (Tamanho do Cesto)'),
        ('valor_medio', 'Valor Médio do Artigo (Mix de Preço)'),
    ]

    supermercado = models.ForeignKey(Supermercado, on_delete=models.CASCADE, related_name='alavancas')
    mes_referencia = models.CharField('Mês de Referência', max_length=50, default='Março 2026')
    venda_total = models.DecimalField('Venda Total (€)', max_digits=12, decimal_places=2, default=120000.00)
    num_clientes_fluxo = models.IntegerField('Fluxo de Clientes (Talões emitidos)', default=8450)
    itens_por_talao = models.DecimalField('Itens por Talão (Cesto Médio)', max_digits=5, decimal_places=2, default=6.80)
    valor_medio_item = models.DecimalField('Valor Médio do Artigo (€)', max_digits=6, decimal_places=2, default=2.08)
    ticket_medio = models.DecimalField('Ticket Médio (€)', max_digits=6, decimal_places=2, default=14.20)
    
    alavanca_ofensora = models.CharField('Alavanca Ofensora (Causa da Queda)', max_length=30, choices=ALAVANCA_CHOICES, default='fluxo')
    variacao_fluxo_pct = models.DecimalField('Variação de Fluxo (%)', max_digits=5, decimal_places=2, default=-8.0)
    variacao_ticket_pct = models.DecimalField('Variação de Ticket (%)', max_digits=5, decimal_places=2, default=+3.2)
    diagnostico_causa = models.TextField('Diagnóstico: Fato vs Hipótese vs Causa')
    
    meta_fluxo = models.IntegerField('Meta Operacional de Fluxo', default=9200)
    meta_itens_talao = models.DecimalField('Meta Itens por Talão', max_digits=5, decimal_places=2, default=7.50)
    meta_valor_item = models.DecimalField('Meta Valor Médio Artigo (€)', max_digits=6, decimal_places=2, default=2.15)

    class Meta:
        verbose_name = 'Alavanca de Venda (Fórmula do Resultado)'
        verbose_name_plural = 'Alavancas de Venda (Fórmula do Resultado)'

    def __str__(self):
        return f"{self.supermercado.nome} - {self.mes_referencia} (Alavanca: {self.get_alavanca_ofensora_display()})"


class PlanoAcaoOperacional(models.Model):
    """
    Execução: Da Estratégia ao Chão de Loja
    Problema → Prioridade → Ação → Responsável → Prazo → Acompanhamento → Resultado
    """
    PRIORIDADE_CHOICES = [
        ('P1', 'P1 - Crítica (Impacto Imediato de Caixa)'),
        ('P2', 'P2 - Alta (Melhoria Estrutural a 15 Dias)'),
        ('P3', 'P3 - Média (Padronização e POPs)'),
    ]
    STATUS_CHOICES = [
        ('pendente', 'Pendente de Início'),
        ('em_execucao', 'Em Execução no Chão de Loja'),
        ('concluido', 'Concluído & Auditado'),
    ]

    supermercado = models.ForeignKey(Supermercado, on_delete=models.CASCADE, related_name='planos_acao')
    problema = models.CharField('Problema Identificado no Diagnóstico', max_length=255)
    prioridade = models.CharField('Nível de Prioridade', max_length=10, choices=PRIORIDADE_CHOICES, default='P1')
    acao = models.TextField('Ação Operacional Concreta (O que fazer)')
    responsavel = models.CharField('Responsável Direto (Quem executa)', max_length=150)
    prazo_dias = models.IntegerField('Prazo de Execução (Dias)', default=7)
    acompanhamento = models.CharField('Rotina de Controlo e Verificação', max_length=200, default='Conferência diária na abertura de loja')
    status = models.CharField('Estado da Execução', max_length=20, choices=STATUS_CHOICES, default='em_execucao')
    resultado_esperado = models.CharField('Resultado Esperado (€ ou %)', max_length=200)
    resultado_medido = models.CharField('Resultado Real Medido no SAF-T', max_length=200, blank=True, null=True)
    criado_em = models.DateTimeField('Data de Criação', default=timezone.now)

    class Meta:
        verbose_name = 'Plano de Ação Operacional'
        verbose_name_plural = 'Planos de Ação Operacionais'
        ordering = ['prioridade', 'status']

    def __str__(self):
        return f"[{self.prioridade}] {self.problema} ({self.responsavel})"


class LayoutSupermercadoItem(models.Model):
    """
    Ferramenta Pública: Layout de Supermercado & Merchandising
    Fluxo do consumidor, setorização de gôndolas, planogramas e pontos quentes.
    """
    ZONA_CHOICES = [
        ('entrada', 'Entrada & Zona de Descompressão (Frutas & Legumes - FLV)'),
        ('central', 'Corredores Centrais (Mercearia Seca & Alimentação Básica)'),
        ('fundo', 'Fundo da Loja (Secções de Destino: Talho & Padaria)'),
        ('checkouts', 'Linha de Caixas & Checkouts (Compras por Impulso)'),
    ]

    zona = models.CharField('Zona da Loja', max_length=30, choices=ZONA_CHOICES)
    titulo = models.CharField('Princípio de Layout & Merchandising', max_length=200)
    conceito_fluxo = models.TextField('Como o Consumidor se Move e Decide')
    estrategia_exposicao = models.TextField('Técnica de Exposição & Planograma')
    impacto_venda = models.CharField('Impacto Estimado no Ticket', max_length=100, default='+8% a +15% de Venda Casada')
    icone = models.CharField('Ícone Lucide', max_length=50, default='layout-grid')

    class Meta:
        verbose_name = 'Diretriz de Layout & Merchandising'
        verbose_name_plural = 'Diretrizes de Layout & Merchandising'

    def __str__(self):
        return f"[{self.get_zona_display()}] {self.titulo}"


class RedeSetorialRanking(models.Model):
    """
    Pilar 4: Terminal do Analista de Inteligência Setorial (/analista)
    Dados estruturados, rankings, quotas de mercado e indicadores do retalho alimentar em Portugal.
    """
    posicao = models.IntegerField('Posição no Ranking', unique=True)
    grupo_insignia = models.CharField('Grupo Económico / Insígnia', max_length=150)
    sede_pais = models.CharField('Origem do Capital', max_length=100, default='Portugal')
    faturacao_anual_milhoes = models.DecimalField('Faturação Anual Estimada (€ Milhões)', max_digits=10, decimal_places=1)
    num_lojas = models.IntegerField('N.º Total de Lojas em Portugal')
    quota_mercado_pct = models.DecimalField('Quota de Mercado Estimada (%)', max_digits=5, decimal_places=2)
    venda_m2_ano = models.DecimalField('Produtividade Média (€/m²/ano)', max_digits=8, decimal_places=0, default=5200)
    tendencia_estrategica = models.CharField('Movimento Estratégico & Tendência', max_length=255)
    arquetipo_operacao = models.CharField('Arquétipo de Operação', max_length=100, default='Supermercado de Proximidade & Hipermercado')

    class Meta:
        verbose_name = 'Ranking de Insígnia (Terminal do Analista)'
        verbose_name_plural = 'Rankings de Insígnias (Terminal do Analista)'
        ordering = ['posicao']

    def __str__(self):
        return f"#{self.posicao} {self.grupo_insignia} ({self.quota_mercado_pct}%)"


class PortalClienteToken(models.Model):
    """
    Ambiente 3: Portal do Cliente (Compartilhamento Seguro por Design)
    Acesso simplificado via token seguro sem navegar na parte administrativa.
    """
    token = models.UUIDField('Token de Acesso Seguro', default=uuid.uuid4, unique=True, editable=False)
    supermercado = models.ForeignKey(Supermercado, on_delete=models.CASCADE, related_name='tokens_acesso')
    destinatario_nome = models.CharField('Nome do Sócio-Gerente / Diretor', max_length=150)
    destinatario_email = models.EmailField('Correio Eletrónico')
    permissoes = models.CharField('Permissões Concedidas', max_length=200, default='bi_dashboards,planos_acao,lancamento_diario')
    ativo = models.BooleanField('Link Ativo', default=True)
    visualizacoes = models.IntegerField('N.º de Acessos Realizados', default=0)
    criado_em = models.DateTimeField('Gerado em', default=timezone.now)
    expira_em = models.DateTimeField('Expira em', blank=True, null=True)

    class Meta:
        verbose_name = 'Token de Acesso do Portal do Cliente'
        verbose_name_plural = 'Tokens de Acesso do Portal do Cliente'

    def __str__(self):
        return f"Token [{self.token}] - {self.supermercado.nome} ({self.destinatario_nome})"


class OportunidadeIndustria(models.Model):
    """
    Pilar 3: Portal da Indústria & Distribuição (/industria)
    Inteligência comercial para fornecedores e grossistas que vendem ao retalho.
    """
    categoria = models.CharField('Categoria de Produto', max_length=150)
    marca_parceira = models.CharField('Marca / Fabricante Representativo', max_length=150)
    regiao_oportunidade = models.CharField('Região com Maior Potencial em Portugal', max_length=150, default='Norte & Centro')
    diagnostico_gondola = models.TextField('Diagnóstico de Linear & Sell-Out')
    potencial_sellout_euros = models.DecimalField('Oportunidade Comercial Mensal (€)', max_digits=10, decimal_places=2)
    taxa_rutura_linear = models.DecimalField('Taxa de Rutura na Prateleira (%)', max_digits=5, decimal_places=2, default=12.5)

    class Meta:
        verbose_name = 'Oportunidade Comercial (Portal da Indústria)'
        verbose_name_plural = 'Oportunidades Comerciais (Portal da Indústria)'

    def __str__(self):
        return f"[{self.categoria}] {self.marca_parceira} - {self.regiao_oportunidade}"


