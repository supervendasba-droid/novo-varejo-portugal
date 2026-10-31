import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import (
    Supermercado, LeadDiagnostico, ArtigoCurvaA, RuturaFantasma, StockMorto,
    ErroIvaSaft, AlertaMobile, RelatorioAuditoria, AreaVerificacao, ChecklistItem, DocumentoConsultoria,
    EmpresaAutomovel, ViaturaStand, OrdemOficina, SegmentoRentACar, AlertaAutomovel,
    AlavancaVenda, PlanoAcaoOperacional, LayoutSupermercadoItem, RedeSetorialRanking,
    PortalClienteToken, OportunidadeIndustria
)

def home_view(request):
    """
    Página Principal da SPA: Novo Varejo Inteligência de Mercado / Regis Costa Consultoria.
    Plataforma de referência para retalho alimentar e supermercados em Portugal.
    """
    supermercado = Supermercado.objects.first()
    artigos_curva_a = ArtigoCurvaA.objects.all()
    ruturas = RuturaFantasma.objects.all()
    stock_morto = StockMorto.objects.all()
    erros_iva = ErroIvaSaft.objects.all()
    alertas = AlertaMobile.objects.all()
    relatorios = RelatorioAuditoria.objects.all()
    areas_verificacao = AreaVerificacao.objects.prefetch_related('itens').all()
    documentos = DocumentoConsultoria.objects.all()

    total_recuperado_precos = sum(
        item.perda_mensal for item in artigos_curva_a if item.atualizado
    )

    context = {
        'supermercado': supermercado,
        'artigos_curva_a': artigos_curva_a,
        'ruturas': ruturas,
        'stock_morto': stock_morto,
        'erros_iva': erros_iva,
        'alertas': alertas,
        'relatorios': relatorios,
        'areas_verificacao': areas_verificacao,
        'documentos': documentos,
        'total_recuperado_precos': total_recuperado_precos,
    }
    return render(request, 'index.html', context)


def dashboard_view(request):
    supermercado = Supermercado.objects.first()
    artigos_curva_a = ArtigoCurvaA.objects.all()
    ruturas = RuturaFantasma.objects.all()
    stock_morto = StockMorto.objects.all()
    erros_iva = ErroIvaSaft.objects.all()
    alertas = AlertaMobile.objects.all()

    total_recuperado_precos = sum(
        item.perda_mensal for item in artigos_curva_a if item.atualizado
    )

    context = {
        'supermercado': supermercado,
        'artigos_curva_a': artigos_curva_a,
        'ruturas': ruturas,
        'stock_morto': stock_morto,
        'erros_iva': erros_iva,
        'alertas': alertas,
        'total_recuperado_precos': total_recuperado_precos,
    }
    return render(request, 'dashboard.html', context)


def relatorios_lista_view(request):
    supermercado = Supermercado.objects.first()
    relatorios = RelatorioAuditoria.objects.all()
    context = {
        'supermercado': supermercado,
        'relatorios': relatorios,
    }
    return render(request, 'relatorios_lista.html', context)


def relatorio_detalhe_view(request, relatorio_id):
    relatorio = get_object_or_404(RelatorioAuditoria, id=relatorio_id)
    context = {
        'relatorio': relatorio,
        'supermercado': relatorio.supermercado,
    }
    return render(request, 'relatorio_detalhe.html', context)


def verificacao_view(request):
    supermercado = Supermercado.objects.first()
    areas = AreaVerificacao.objects.prefetch_related('itens').all()
    todos_itens = ChecklistItem.objects.all()
    total_itens = todos_itens.count()
    total_conforme = todos_itens.filter(status='conforme').count()
    total_inconforme = todos_itens.filter(status='nao_conforme').count()
    total_correcao = todos_itens.filter(status='em_correcao').count()
    taxa_conformidade = round((total_conforme / total_itens * 100), 1) if total_itens > 0 else 100.0

    context = {
        'supermercado': supermercado,
        'areas': areas,
        'total_itens': total_itens,
        'total_conforme': total_conforme,
        'total_inconforme': total_inconforme,
        'total_correcao': total_correcao,
        'taxa_conformidade': taxa_conformidade,
    }
    return render(request, 'verificacao.html', context)


def documentos_view(request):
    supermercado = Supermercado.objects.first()
    documentos = DocumentoConsultoria.objects.all()
    context = {
        'supermercado': supermercado,
        'documentos': documentos,
    }
    return render(request, 'documentos.html', context)


# ==========================================
# ENDPOINTS REST / AJAX INTERATIVOS
# ==========================================

@require_POST
def api_toggle_pvp(request, artigo_id=None):
    if artigo_id == 0 or artigo_id is None:
        try:
            data = json.loads(request.body)
            novo_estado = data.get('estado', True)
        except Exception:
            novo_estado = True
        ArtigoCurvaA.objects.all().update(atualizado=novo_estado)
        total_recuperado = sum(item.perda_mensal for item in ArtigoCurvaA.objects.filter(atualizado=True))
        return JsonResponse({
            'success': True,
            'global': True,
            'estado': novo_estado,
            'total_recuperado': float(total_recuperado),
            'mensagem': 'Simulação POS ativa: +1.850,00 €/mês em margem de reposição blindada!' if novo_estado else 'Valores originais repostos na loja.'
        })

    try:
        artigo = ArtigoCurvaA.objects.get(id=artigo_id)
        artigo.atualizado = not artigo.atualizado
        artigo.save()
        total_recuperado = sum(item.perda_mensal for item in ArtigoCurvaA.objects.filter(atualizado=True))
        return JsonResponse({
            'success': True,
            'artigo_id': artigo.id,
            'atualizado': artigo.atualizado,
            'total_recuperado': float(total_recuperado),
            'mensagem': f"PVP de {artigo.artigo} blindado no POS!" if artigo.atualizado else f"PVP de {artigo.artigo} restaurado."
        })
    except ArtigoCurvaA.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Artigo não localizado'}, status=404)


@require_POST
def api_resolver_rutura(request, rutura_id):
    try:
        rutura = RuturaFantasma.objects.get(id=rutura_id)
        rutura.resolvido = not rutura.resolvido
        rutura.save()
        return JsonResponse({
            'success': True,
            'rutura_id': rutura.id,
            'resolvido': rutura.resolvido,
            'mensagem': f"Ordem de reposição emitida no linear para {rutura.artigo}!" if rutura.resolvido else f"Rutura de {rutura.artigo} reaberta."
        })
    except RuturaFantasma.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Registo não localizado'}, status=404)


@require_POST
def api_corrigir_iva(request, erro_id):
    try:
        erro = ErroIvaSaft.objects.get(id=erro_id)
        erro.corrigido = not erro.corrigido
        erro.save()
        return JsonResponse({
            'success': True,
            'erro_id': erro.id,
            'corrigido': erro.corrigido,
            'mensagem': f"Taxa de IVA do artigo {erro.codigo} saneada no cadastro POS!" if erro.corrigido else f"Artigo {erro.codigo} marcado como pendente de conferência."
        })
    except ErroIvaSaft.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Registo não localizado'}, status=404)


@require_POST
def api_toggle_checklist_item(request, item_id):
    try:
        data = json.loads(request.body)
        novo_status = data.get('status', 'conforme')
        item = ChecklistItem.objects.get(id=item_id)
        item.status = novo_status
        item.save()
        
        todos = ChecklistItem.objects.all()
        total = todos.count()
        conformes = todos.filter(status='conforme').count()
        taxa = round((conformes / total * 100), 1) if total > 0 else 100.0

        return JsonResponse({
            'success': True,
            'item_id': item.id,
            'status': item.status,
            'taxa_conformidade': taxa,
            'mensagem': f"Ponto de controlo atualizado: {item.ponto_verificacao[:30]}..."
        })
    except ChecklistItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item não localizado'}, status=404)


@csrf_exempt
@require_POST
def api_calcular_diagnostico(request):
    """
    Calculadora avançada de fugas invisíveis para retalho em Portugal.
    Calcula perdas em frescos (40%), erosão de PVP (31%), roturas virtuais (18%) e IVA (11%).
    """
    try:
        data = json.loads(request.body)
        faturacao = float(data.get('faturacao', 120000))
        caixas = int(data.get('caixas', 3))
        colaboradores = int(data.get('colaboradores', 14))

        # Benchmark de mercado em Portugal: taxa de fuga média de 5,0% sobre faturação líquida
        fuga_mensal_total = faturacao * 0.05
        fuga_anual_total = fuga_mensal_total * 12

        fuga_frescos = fuga_mensal_total * 0.40
        fuga_precos = fuga_mensal_total * 0.31
        fuga_roturas = fuga_mensal_total * 0.18
        fuga_iva = fuga_mensal_total * 0.11

        potencial_recuperacao_65 = fuga_mensal_total * 0.65
        retorno_liquido_ano = (potencial_recuperacao_65 - 1500) * 12 + 1000

        # Se vierem dados de lead, salva no banco
        nome = data.get('nome', '').strip()
        empresa = data.get('empresa', '').strip()
        email = data.get('email', '').strip()
        telemovel = data.get('telemovel', '').strip()
        concelho = data.get('concelho', '').strip()

        lead_id = None
        if nome and (email or telemovel):
            lead = LeadDiagnostico.objects.create(
                nome=nome,
                empresa=empresa or f"Supermercado ({concelho or 'Portugal'})",
                email=email,
                telemovel=telemovel,
                distrito=concelho or 'Portugal',
                lojas=f"{caixas} postos de caixa",
                faturacao=f"{faturacao:,.0f} € / mês",
                mensagem=f"Simulação via Calculadora: {colaboradores} colaboradores, {caixas} caixas. Fuga estimada: {fuga_mensal_total:,.0f} €/mês.",
                status='novo'
            )
            lead_id = lead.id

        return JsonResponse({
            'success': True,
            'lead_id': lead_id,
            'faturacao': faturacao,
            'fuga_mensal': round(fuga_mensal_total, 2),
            'fuga_anual': round(fuga_anual_total, 2),
            'fuga_diaria': round(fuga_mensal_total / 30, 2),
            'fuga_frescos': round(fuga_frescos, 2),
            'fuga_precos': round(fuga_precos, 2),
            'fuga_roturas': round(fuga_roturas, 2),
            'fuga_iva': round(fuga_iva, 2),
            'recuperacao_mensal_esperada': round(potencial_recuperacao_65, 2),
            'ganho_liquido_ano': round(retorno_liquido_ano, 2),
            'mensagem': 'Cálculo de pré-diagnóstico concluído com sucesso!'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_POST
def api_solicitar_diagnostico(request):
    try:
        data = json.loads(request.body)
        lead = LeadDiagnostico.objects.create(
            nome=data.get('nome', '').strip(),
            empresa=data.get('empresa', '').strip(),
            nif=data.get('nif', '').strip(),
            email=data.get('email', '').strip(),
            telemovel=data.get('telemovel', '').strip(),
            distrito=data.get('distrito', 'Lisboa e Vale do Tejo'),
            lojas=data.get('lojas', '1 a 3 lojas'),
            faturacao=data.get('faturacao', '100.000 € a 250.000 €'),
            software_pos=data.get('software_pos', ''),
            mensagem=data.get('mensagem', '').strip(),
        )
        return JsonResponse({
            'success': True,
            'lead_id': lead.id,
            'mensagem': 'Solicitação de Diagnóstico Raio-X 360º registada com sucesso! O nosso Consultor Principal entrará em contacto nas próximas 2 horas úteis.'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ==============================================================================
# MÓDULO DE CONSULTORIA AUTOMÓVEL & MOBILIDADE (STAND + OFICINA + RENT-A-CAR)
# ==============================================================================

def automovel_view(request):
    """
    Página Executiva & Dashboard de BI para Concessionárias, Oficinas e Rent-a-Car em Portugal.
    Audita os 3 polos: Stand (Aging & Margem), Oficina (Horas & Peças) e Rent-a-car (Ocupação & RevPAV).
    """
    empresa = EmpresaAutomovel.objects.first()
    viaturas = ViaturaStand.objects.all()
    ordens = OrdemOficina.objects.all()
    segmentos = SegmentoRentACar.objects.all()
    alertas = AlertaAutomovel.objects.all()

    # Cálculos Consolidados
    total_viaturas_stand = viaturas.count()
    viaturas_curva_c = viaturas.filter(dias_em_stock__gte=60)
    capital_imobilizado_stand = sum(v.custo_aquisicao + v.custo_recondicionamento for v in viaturas)
    capital_preso_curva_c = sum(v.custo_aquisicao + v.custo_recondicionamento for v in viaturas_curva_c)
    custo_floor_plan_total = sum(v.custo_financeiro_parado for v in viaturas)

    # Oficina
    horas_perdidas_total = sum(o.horas_orcamentadas - o.horas_faturadas for o in ordens)
    perda_margem_pecas_total = sum(o.perda_margem_pecas for o in ordens)

    # Rent-a-car
    total_carros_frota = sum(s.qtd_viaturas for s in segmentos)
    ocupacao_media = sum(s.taxa_ocupacao_atual * s.qtd_viaturas for s in segmentos) / (total_carros_frota or 1)

    context = {
        'empresa': empresa,
        'viaturas': viaturas,
        'ordens': ordens,
        'segmentos': segmentos,
        'alertas': alertas,
        'total_viaturas_stand': total_viaturas_stand,
        'viaturas_curva_c_count': viaturas_curva_c.count(),
        'capital_imobilizado_stand': capital_imobilizado_stand,
        'capital_preso_curva_c': capital_preso_curva_c,
        'custo_floor_plan_total': custo_floor_plan_total,
        'horas_perdidas_total': horas_perdidas_total,
        'perda_margem_pecas_total': perda_margem_pecas_total,
        'total_carros_frota': total_carros_frota,
        'ocupacao_media': round(ocupacao_media, 1),
    }
    return render(request, 'automovel.html', context)


@csrf_exempt
@require_POST
def api_toggle_desagio(request, viatura_id):
    """
    Alterna a aplicação de deságio estratégico de preço para acelerar giro de viatura na Curva C.
    """
    try:
        viatura = get_object_or_404(ViaturaStand, id=viatura_id)
        viatura.desagio_aplicado = not viatura.desagio_aplicado
        viatura.save()

        novo_pvp = viatura.pvp_desagio_sugerido if viatura.desagio_aplicado else viatura.pvp_anunciado
        msg = f"Deságio ativado para {viatura.viatura}: Novo PVP {novo_pvp} € (Libertação de tesouraria em curso)." if viatura.desagio_aplicado else f"Preço de tabela restabelecido para {viatura.viatura}."

        return JsonResponse({
            'success': True,
            'viatura_id': viatura.id,
            'desagio_aplicado': viatura.desagio_aplicado,
            'novo_pvp': float(novo_pvp),
            'mensagem': msg
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@csrf_exempt
@require_POST
def api_calcular_diagnostico_auto(request):
    """
    Simulador interativo de potencial de recuperação para negócios automotivos (Stand + Oficina + Rent-a-Car).
    """
    try:
        data = json.loads(request.body)
        fat_stand = float(data.get('faturacao_stand', 220000))
        fat_oficina = float(data.get('faturacao_oficina', 95000))
        fat_rent = float(data.get('faturacao_rentacar', 65000))
        carros_stock = int(data.get('carros_stock', 35))
        elevadores = int(data.get('elevadores', 6))
        frota_rent = int(data.get('frota_rent', 48))

        # Modelagem de perdas médias auditadas em Portugal:
        # Stand: 2.8% da faturação em juros de floor plan e desvalorização por carros parados > 60 dias
        perda_stand = fat_stand * 0.028
        # Oficina: 5.4% da faturação em horas não faturadas vs pagas e margem de peças erodida
        perda_oficina = fat_oficina * 0.054
        # Rent-a-Car: 5.3% da faturação em taxa de ocupação subótima e desmobilização tardia
        perda_rent = fat_rent * 0.053
        # Fiscal: Média de 1.200 €/mês em Tributação Autónoma mal enquadrada e IVA da margem
        perda_fiscal = 1200.0

        perda_total_mes = perda_stand + perda_oficina + perda_rent + perda_fiscal
        recuperacao_estimada_mes = perda_total_mes * 0.68  # 68% de meta realista
        ganho_liquido_ano = (recuperacao_estimada_mes - 1800.0) * 12  # Avença média de 1.800€

        return JsonResponse({
            'success': True,
            'faturacao_global': fat_stand + fat_oficina + fat_rent,
            'perda_total_mes': round(perda_total_mes, 2),
            'perda_total_ano': round(perda_total_mes * 12, 2),
            'perda_stand': round(perda_stand, 2),
            'perda_oficina': round(perda_oficina, 2),
            'perda_rent': round(perda_rent, 2),
            'perda_fiscal': round(perda_fiscal, 2),
            'recuperacao_estimada_mes': round(recuperacao_estimada_mes, 2),
            'ganho_liquido_ano': round(ganho_liquido_ano, 2),
            'mensagem': 'Diagnóstico de auditoria automotiva calculado com sucesso!'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ==============================================================================
# NOVAS FUNCIONALIDADES DO ECOSSISTEMA NOVO VAREJO (METODOLOGIA COMPLETA)
# ==============================================================================

def alavancas_view(request):
    """
    Pilar 1: As Alavancas da Venda (A Fórmula do Resultado)
    Venda = Clientes (Fluxo) × Ticket Médio (Itens por Talão × Valor Médio do Artigo)
    """
    supermercado = Supermercado.objects.first()
    alavanca = AlavancaVenda.objects.first()
    planos = PlanoAcaoOperacional.objects.all()

    context = {
        'supermercado': supermercado,
        'alavanca': alavanca,
        'planos': planos,
    }
    return render(request, 'alavancas.html', context)


def layout_view(request):
    """
    Ferramenta Pública: Layout de Supermercado & Merchandising
    Fluxo do consumidor, planograma, pontos quentes e setorização de gôndolas.
    """
    supermercado = Supermercado.objects.first()
    layouts = LayoutSupermercadoItem.objects.all()

    context = {
        'supermercado': supermercado,
        'layouts': layouts,
    }
    return render(request, 'layout.html', context)


def analista_view(request):
    """
    Pilar 4: Terminal do Analista de Inteligência Setorial (/analista)
    Rankings das 8 maiores redes em Portugal, quota de mercado, faturamento e tendências.
    """
    rankings = RedeSetorialRanking.objects.all()
    total_faturacao_mercado = sum(r.faturacao_anual_milhoes for r in rankings)

    context = {
        'rankings': rankings,
        'total_faturacao_mercado': total_faturacao_mercado,
        'total_redes': rankings.count(),
    }
    return render(request, 'analista.html', context)


def industria_view(request):
    """
    Pilar 3: Portal da Indústria & Distribuição (/industria)
    Inteligência comercial B2B para fornecedores, fabricantes e grossistas do retalho alimentar.
    """
    oportunidades = OportunidadeIndustria.objects.all()
    total_oportunidade = sum(o.potencial_sellout_euros for o in oportunidades)

    context = {
        'oportunidades': oportunidades,
        'total_oportunidade': total_oportunidade,
    }
    return render(request, 'industria.html', context)


def gestao_view(request):
    """
    Ambiente 2: Área de Gestão do Consultor
    Plataforma autenticada com carteira de clientes, lojas e planos de ação operacionais.
    """
    supermercado = Supermercado.objects.first()
    planos = PlanoAcaoOperacional.objects.all()
    alavanca = AlavancaVenda.objects.first()
    token_obj = PortalClienteToken.objects.first()

    context = {
        'supermercado': supermercado,
        'planos': planos,
        'alavanca': alavanca,
        'token_obj': token_obj,
    }
    return render(request, 'gestao.html', context)


def portal_cliente_view(request, token):
    """
    Ambiente 3: Portal do Cliente com Link Seguro (Compartilhamento Seguro por Design)
    Acesso direto do sócio-gerente/equipe ao plano de ação e métricas autorizadas.
    """
    token_obj = get_object_or_404(PortalClienteToken, token=token, ativo=True)
    token_obj.visualizacoes += 1
    token_obj.save()

    supermercado = token_obj.supermercado
    planos = PlanoAcaoOperacional.objects.filter(supermercado=supermercado)
    alavanca = AlavancaVenda.objects.filter(supermercado=supermercado).first()

    context = {
        'token_obj': token_obj,
        'supermercado': supermercado,
        'planos': planos,
        'alavanca': alavanca,
    }
    return render(request, 'portal_cliente.html', context)


@csrf_exempt
@require_POST
def api_toggle_plano_acao(request, plano_id):
    """
    Atualiza o estado de um plano de ação (pendente -> em_execucao -> concluido).
    """
    try:
        plano = get_object_or_404(PlanoAcaoOperacional, id=plano_id)
        if plano.status == 'concluido':
            plano.status = 'em_execucao'
        elif plano.status == 'em_execucao':
            plano.status = 'concluido'
        else:
            plano.status = 'em_execucao'
        plano.save()

        return JsonResponse({
            'success': True,
            'plano_id': plano.id,
            'novo_status': plano.status,
            'status_display': plano.get_status_display(),
            'mensagem': f"Plano atualizado para: {plano.get_status_display()}"
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


