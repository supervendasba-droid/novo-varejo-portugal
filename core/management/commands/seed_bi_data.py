from django.core.management.base import BaseCommand
from core.models import (
    Supermercado, ArtigoCurvaA, RuturaFantasma, StockMorto, ErroIvaSaft,
    AlertaMobile, RelatorioAuditoria, AreaVerificacao, ChecklistItem, DocumentoConsultoria
)

class Command(BaseCommand):
    help = 'Popula a base de dados de consultoria para supermercados em Portugal com relatórios, checklists e minutas'

    def handle(self, *args, **options):
        # 1. Supermercado Cliente Matriz
        supermercado, _ = Supermercado.objects.update_or_create(
            nif='509876543',
            defaults={
                'nome': 'Supermercado da Vila Lda.',
                'razao_social': 'Supermercado da Vila - Distribuição Alimentar, Lda.',
                'localizacao': 'Sintra / Área Metropolitana de Lisboa',
                'area_m2': 400,
                'num_caixas': 3,
                'num_colaboradores': 14,
                'software_pos': 'ETPOS Enterprise',
                'faturacao_mensal': 120000.00,
                'margem_teorica': 24.50,
                'margem_real': 19.50,
            }
        )

        # 2. Artigos Curva A
        artigos_data = [
            {
                'codigo': 'PT001',
                'ean': '5601012001428',
                'artigo': 'Azeite Virgem Extra Oliveira da Serra 75cl',
                'familia': 'Mercearia / Azeites',
                'custo_medio_pos': 4.55,
                'custo_ultima_fatura': 5.25,
                'pvp_atual': 6.49,
                'pvp_sugerido': 7.29,
                'iva': 6,
                'volume_mensal': 380,
                'perda_mensal': 266.00,
                'fornecedor': 'Sovena Portugal / Grossista MARL'
            },
            {
                'codigo': 'PT002',
                'ean': '5602345112098',
                'artigo': 'Bacalhau Crescido da Noruega 1ª (kg)',
                'familia': 'Charcutaria / Salgados',
                'custo_medio_pos': 9.80,
                'custo_ultima_fatura': 11.40,
                'pvp_atual': 13.99,
                'pvp_sugerido': 15.99,
                'iva': 6,
                'volume_mensal': 260,
                'perda_mensal': 416.00,
                'fornecedor': 'Riberalves / MARL'
            },
            {
                'codigo': 'PT003',
                'ean': '5601008100258',
                'artigo': 'Café Delta Lote Chávena Moído 250g',
                'familia': 'Mercearia / Cafés',
                'custo_medio_pos': 2.35,
                'custo_ultima_fatura': 2.78,
                'pvp_atual': 3.49,
                'pvp_sugerido': 3.99,
                'iva': 23,
                'volume_mensal': 520,
                'perda_mensal': 223.60,
                'fornecedor': 'Nabeiro / Delta Cafés'
            },
            {
                'codigo': 'PT004',
                'ean': '5601234998712',
                'artigo': 'Óleo Alimentar Fula Puro Girassol 1L',
                'familia': 'Mercearia / Óleos',
                'custo_medio_pos': 1.58,
                'custo_ultima_fatura': 1.89,
                'pvp_atual': 2.29,
                'pvp_sugerido': 2.69,
                'iva': 6,
                'volume_mensal': 490,
                'perda_mensal': 151.90,
                'fornecedor': 'Recheio Cash & Carry'
            },
            {
                'codigo': 'PT005',
                'ean': '5601038001129',
                'artigo': 'Leite UHT Mimosa Meio Gordo 1L',
                'familia': 'Lacticínios',
                'custo_medio_pos': 0.72,
                'custo_ultima_fatura': 0.84,
                'pvp_atual': 0.99,
                'pvp_sugerido': 1.14,
                'iva': 6,
                'volume_mensal': 1850,
                'perda_mensal': 222.00,
                'fornecedor': 'Lactogal Portugal'
            },
            {
                'codigo': 'PT006',
                'ean': '5601154887210',
                'artigo': 'Vinho Tinto Esteva Douro 75cl (Garrafeira)',
                'familia': 'Garrafeira / Vinhos',
                'custo_medio_pos': 3.10,
                'custo_ultima_fatura': 3.75,
                'pvp_atual': 4.99,
                'pvp_sugerido': 5.89,
                'iva': 13,
                'volume_mensal': 310,
                'perda_mensal': 201.50,
                'fornecedor': 'Sogrape Distribuição'
            },
            {
                'codigo': 'PT007',
                'ean': '5601876543219',
                'artigo': 'Ovos Frescos Classe L Dúzia (Matinados)',
                'familia': 'Mercearia / Frescos',
                'custo_medio_pos': 1.85,
                'custo_ultima_fatura': 2.25,
                'pvp_atual': 2.69,
                'pvp_sugerido': 3.19,
                'iva': 6,
                'volume_mensal': 920,
                'perda_mensal': 369.00,
                'fornecedor': 'Grupo Valouro'
            }
        ]
        for item in artigos_data:
            ArtigoCurvaA.objects.update_or_create(codigo=item['codigo'], defaults=item)

        # 3. Ruturas Fantasma
        ruturas_data = [
            {
                'codigo': 'RF01',
                'artigo': 'Leite UHT Mimosa Meio Gordo 1L (Pack 6)',
                'stock_sistema': 48,
                'horas_sem_venda': '51h (Desde 3.ª feira 14h00)',
                'causa_provavel': 'Palete bloqueada no armazém traseiro sem reposição no linear',
                'perda_estimada_mes': 320.00
            },
            {
                'codigo': 'RF02',
                'artigo': 'Cerveja Super Bock Mini 20cl (Grade 24 un.)',
                'stock_sistema': 19,
                'horas_sem_venda': '48h (Zero leituras no POS)',
                'causa_provavel': 'Erro de inventário / Furto ou quebra não abatida formalmente',
                'perda_estimada_mes': 290.00
            },
            {
                'codigo': 'RF03',
                'artigo': 'Atum Bom Petisco em Azeite 120g',
                'stock_sistema': 64,
                'horas_sem_venda': '62h (Sem saída na caixa)',
                'causa_provavel': 'Artigo sem etiqueta de PVP visível no linear (cliente não leva)',
                'perda_estimada_mes': 215.00
            },
            {
                'codigo': 'RF04',
                'artigo': 'Água Luso Sem Gás Garrafão 5,4L',
                'stock_sistema': 32,
                'horas_sem_venda': '49h (Sem saída na caixa)',
                'causa_provavel': 'Código de barras de unidade trocado com código de pack no ETPOS',
                'perda_estimada_mes': 275.00
            }
        ]
        for item in ruturas_data:
            RuturaFantasma.objects.update_or_create(codigo=item['codigo'], defaults=item)

        # 4. Stock Morto
        stock_morto_data = [
            {
                'categoria': 'Garrafeira Reserva e Espirituosas de Baixo Giro',
                'skus': 118,
                'dias_sem_venda': '112 dias',
                'capital_imobilizado': 6450.00,
                'sugestao': 'Feira de Vinhos de Fim de Semana (-25% PVP) com topo de linear'
            },
            {
                'categoria': 'Higiene e Perfumaria (Marcas Duplicadas)',
                'skus': 340,
                'dias_sem_venda': '84 dias',
                'capital_imobilizado': 5200.00,
                'sugestao': 'Pack Promocional Leve 2 Pague 1 na Cabeceira da Linha de Caixas'
            },
            {
                'categoria': 'Bazar, Utilidades Domésticas e Sazonais',
                'skus': 495,
                'dias_sem_venda': '145 dias',
                'capital_imobilizado': 4150.00,
                'sugestao': 'Cesto de Liquidação Direta a 1 € e 2 € junto à Entrada de Loja'
            },
            {
                'categoria': 'Mercearia Gourmet e Conservas Importadas',
                'skus': 210,
                'dias_sem_venda': '68 dias',
                'capital_imobilizado': 2700.00,
                'sugestao': 'Desconto de Escoamento + Exclusão Definitiva do Cadastro de Compras'
            }
        ]
        for item in stock_morto_data:
            StockMorto.objects.update_or_create(categoria=item['categoria'], defaults=item)

        # 5. Divergências de IVA SAF-T
        erros_iva_data = [
            {
                'codigo': 'ART-4092',
                'descricao': 'Sumo Compal Clássico Pêssego 1L (Néctar)',
                'iva_compra': '23%',
                'iva_venda_pos': '6%',
                'diferenca': '17%',
                'prejuizo_mensal': 210.00
            },
            {
                'codigo': 'ART-1184',
                'descricao': 'Queijo Flamengo Fatiado Embalado (Transformado)',
                'iva_compra': '13%',
                'iva_venda_pos': '6%',
                'diferenca': '7%',
                'prejuizo_mensal': 145.00
            },
            {
                'codigo': 'ART-8831',
                'descricao': 'Vinho Verde Branco Casal Garcia 75cl',
                'iva_compra': '13%',
                'iva_venda_pos': '6%',
                'diferenca': '7%',
                'prejuizo_mensal': 175.00
            },
            {
                'codigo': 'ART-5520',
                'descricao': 'Sacos de Compras Reutilizáveis Ráfia (Linha Caixa)',
                'iva_compra': '23%',
                'iva_venda_pos': 'Isento (0%)',
                'diferenca': '23%',
                'prejuizo_mensal': 120.00
            }
        ]
        for item in erros_iva_data:
            ErroIvaSaft.objects.update_or_create(codigo=item['codigo'], defaults=item)

        # 6. Alertas Mobile (WhatsApp)
        alertas_data = [
            {
                'tipo': 'Cais de Receção • Inflação de Custo',
                'hora': 'Hoje, 08:42',
                'canal': 'WhatsApp Gerência',
                'mensagem': 'Atenção Sr. Manuel: A fatura n.º 4520 do grossista subiu o custo do Azeite Oliveira da Serra 75cl em +15,3% (para 5,25 €). Se mantiver o PVP atual de 6,49 €, perderá 266 € de margem neste lote. PVP sugerido: 7,29 €.',
                'ecra_destino': 'precos'
            },
            {
                'tipo': 'Chão de Loja • Rutura Fantasma Curva A',
                'hora': 'Hoje, 10:15',
                'canal': 'Alerta Chefe de Loja',
                'mensagem': 'Stock Virtual Detetado: O artigo Leite UHT Mimosa Meio Gordo consta com 48 unidades no sistema POS, mas regista ZERO vendas na linha de caixa há 51 horas. Verificar palete no armazém.',
                'ecra_destino': 'stock'
            },
            {
                'tipo': 'Secção de Frescos • Quebra Oculta FLV',
                'hora': 'Ontem, 19:30',
                'canal': 'Controlo de Perecíveis',
                'mensagem': 'Alerta Operacional: A secção de Frutas e Legumes (FLV) não registou nenhum auto de abate de quebra nos últimos 3 dias. Risco de distorção grave no stock informático e CMVC.',
                'ecra_destino': 'frescos'
            },
            {
                'tipo': 'Auditoria SAF-T (PT) • Divergência de IVA',
                'hora': 'Há 2 dias',
                'canal': 'Ponte Contabilista (CC)',
                'mensagem': 'Conformidade Autoridade Tributária: Detetados 38 artigos no cadastro com compra a IVA de 23%/13% e saída na caixa parametrizada a 6%. Perda fiscal de 650 €/mês.',
                'ecra_destino': 'contabil'
            }
        ]
        for item in alertas_data:
            AlertaMobile.objects.update_or_create(tipo=item['tipo'], defaults=item)

        # 7. Relatórios Oficiais de Auditoria
        relatorios_data = [
            {
                'supermercado': supermercado,
                'tipo': 'cmvc',
                'codigo_doc': 'REL-CMVC-2026-10',
                'titulo': 'Relatório Mensal de Apuramento do CMVC e Margem Comercial Real',
                'periodo': 'Outubro de 2026',
                'valor_impacto': 6000.00,
                'resumo_executivo': 'A auditoria analítica ao ficheiro SAF-T (PT) e balancete de encerramento revelou um desvio de 5,0 pontos percentuais entre a margem bruta de sistema (24,5%) e a margem real de caixa (19,5%). A hemorragia mensal fixa-se em 6.000 €/mês (72.000 € anuais), concentrada em quebras de perecíveis não abatidas formalmente e na erosão por atraso na reindexação de PVPs.',
                'parecer_consultor': '1. Reindexar imediatamente os 142 artigos da Curva A com base no custo da última fatura do cais (+1.850 €/mês recuperáveis).\n2. Emitir obrigatoriamente autos de abate diários nos frescos para regularização de inventário perante a AT.\n3. Implementar protocolo de receção cega no cais para evitar faturas superiores ao acordado com grossistas.',
                'destinatario': 'Gerência Executiva & Contabilista Certificado (CC)',
                'assinado_por': 'Dr. Carlos Ramos, ROC / Consultor Principal de Retalho'
            },
            {
                'supermercado': supermercado,
                'tipo': 'auto_quebras',
                'codigo_doc': 'AUTO-ABATE-2026-W44',
                'titulo': 'Auto Oficial de Abate de Quebras e Destruição de Mercadoria (Art.º 86.º CIVA)',
                'periodo': 'Semana 44 / Outubro 2026',
                'valor_impacto': 2400.00,
                'resumo_executivo': 'Documento formal de abate de quebras e quebras técnicas para efeitos de dedução fiscal de perdas em sede de IRC e IVA, nos termos do n.º 1 do art.º 86.º do Código do IVA. O lote inclui perdas de desmanche de novilho (osso e sebo desprovido de valor comercial), quebras de perecimento em FLV e quebras acidentais de garrafeira.',
                'parecer_consultor': 'O presente auto cumpre integralmente os requisitos formais exigidos pela Autoridade Tributária e Aduaneira (AT). Deverá ser assinado pelo Sócio-Gerente e pelo Encarregado de Frescos e remetido ao Gabinete de Contabilidade para dedução no CMVC do período.',
                'destinatario': 'Contabilidade Certificada (CC) & Arquivo Fiscal da Empresa',
                'assinado_por': 'Eng.ª Marta Silveira • Auditora Operacional de Frescos'
            },
            {
                'supermercado': supermercado,
                'tipo': 'saf_t',
                'codigo_doc': 'AUD-SAFT-2026-Q3',
                'titulo': 'Auditoria de Conformidade Fiscal SAF-T (PT) e Saneamento de IVA',
                'periodo': '3.º Trimestre de 2026',
                'valor_impacto': 650.00,
                'resumo_executivo': 'Detetadas 38 incongruências graves no cadastro de artigos do software de ponto de venda (POS). Artigos tributados à entrada na taxa normal (23%) ou intermédia (13%) foram faturados ao consumidor final com aplicação errónea da taxa reduzida (6%). Risco direto de infração tributária e distorção na declaração periódica de IVA.',
                'parecer_consultor': 'Procedeu-se à retificação em base de dados de todas as 38 famílias incoerentes. Recomenda-se bloquear a criação de novos artigos na loja sem validação central do código de IVA pelo Contabilista Certificado.',
                'destinatario': 'Gabinete de Contabilidade & Gerência',
                'assinado_por': 'Dr. Carlos Ramos • Consultor Tributário e Financeiro'
            },
            {
                'supermercado': supermercado,
                'tipo': 'equipa',
                'codigo_doc': 'AUD-RH-2026-10',
                'titulo': 'Auditoria de Eficiência Laboral, Custos com Pessoal e Escalas Horárias',
                'periodo': 'Outubro de 2026',
                'valor_impacto': 1200.00,
                'resumo_executivo': 'O custo global com pessoal (14 colaboradores, considerando salários base, subsídios de férias e Natal, e TSU patronal de 23,75%) atinge 17.040 €/mês, representando 14,2% da faturação líquida (acima do benchmark saudável de 11,5% a 12,5%). A faturação média por operador situa-se em 8.571 €/mês, revelando subaproveitamento nos períodos de terça a quinta de manhã.',
                'parecer_consultor': 'Readequação das escalas de caixa: transferir 3 operadores das manhãs de baixo movimento para o horário de pico (17h30 - 19h30). Alocação de 40 horas anuais de formação obrigatória em atendimento no talho e técnicas de conferência de cais.',
                'destinatario': 'Direção de Recursos Humanos e Gerência',
                'assinado_por': 'Dra. Helena Tavares • Consultora de Organização e RH Retalho'
            }
        ]
        for rel in relatorios_data:
            RelatorioAuditoria.objects.update_or_create(codigo_doc=rel['codigo_doc'], defaults=rel)

        # 8. Áreas de Verificação e Checklists de Chão de Loja
        areas_data = [
            {
                'nome': 'Cais de Receção de Mercadorias',
                'icone': 'truck',
                'responsavel_padrao': 'Encarregado de Cais / Armazém',
                'descricao': 'Auditoria à porta de entrada de valor do supermercado. Garante que nada entra na loja sem pesagem rigorosa, temperatura conforme e confronto de preços com as faturas dos grossistas.',
                'ordem': 1,
                'itens': [
                    ('Conferência cega das quantidades recebidas vs. Guia de Remessa', 'O operador deve contar e registar as unidades físicas sem consultar previamente a quantidade declarada na fatura do fornecedor.', 'Risco de pagar mercadoria em falta no ato da entrega (perda imediata de tesouraria).', 'conforme', 'Por cada descarga'),
                    ('Pesagem obrigatória de carcaças de novilho e peças em vácuo no gancho', 'Todas as carcaças e peças devem ser pesadas na balança aérea do cais antes de assinar a guia do transportador.', 'Diferença de peso de 2 a 5 kg por carcaça imputada à loja.', 'conforme', 'Por cada receção'),
                    ('Medição da temperatura no ato da descarga (Termómetro de Sonda)', 'Registo de temperatura em carnes frescas (<= 7ºC), aves (<= 4ºC) e ultracongelados (<= -18ºC).', 'Inconformidade sanitária ASAE e quebra prematura de validade.', 'conforme', 'Diária'),
                    ('Confronto do preço unitário da fatura com a tabela acordada', 'Verificar se o grossista subiu o custo unitário sem aviso prévio antes de aceitar a mercadoria.', 'Erosão de margem invisível no ato da entrada.', 'em_correcao', 'Diária')
                ]
            },
            {
                'nome': 'Secção de Talho & Preparação',
                'icone': 'scissors',
                'responsavel_padrao': 'Chefe de Talho / Cortador Principal',
                'descricao': 'Auditoria ao setor mais sensível de perecíveis. Controlo de rendimento de desmanche, separação de osso e sebo, e eliminação de taras erróneas nas balanças.',
                'ordem': 2,
                'itens': [
                    ('Aplicação rigorosa da Ficha Técnica de Desmanche de Carcaça', 'Calcular o custo real do kg limpo após dedução de 24% a 28% de osso e sebo para cálculo do PVP de venda.', 'Prejuízo de 200 € a 400 € por cada carcaça vendida no olhómetro.', 'conforme', 'Por lote desmanchado'),
                    ('Aferição do desconto automático de tara nas balanças de atendimento', 'Verificar se as balanças deduzem a tara correta do papel sulfurizado (12g) e embalagens de esferovite (18g).', 'Venda de tara a preço de carne nobre ou prejuízo por excesso de tara.', 'conforme', 'Diária (Abertura)'),
                    ('Aproveitamento de aparas nobres para carne picada e preparados', 'As aparas limpas de novilho e suíno devem ser transformadas no próprio dia em hambúrgueres e almôndegas.', 'Descarte indevido de produto nobre como quebra ou sebo.', 'conforme', 'Diária'),
                    ('Registo obrigatório de osso e sebo para recolha de subprodutos (DGV)', 'Toda a quebra de osso deve ser pesada e anotada no diário de corte antes de seguir para os contentores de recolha.', 'Incapacidade de justificar quebras de inventário ao Contabilista.', 'em_correcao', 'Diária (Fecho)')
                ]
            },
            {
                'nome': 'Frutas e Legumes (FLV)',
                'icone': 'apple',
                'responsavel_padrao': 'Encarregado de Frutas e Legumes',
                'descricao': 'Controlo diário do desperdício biológico. Implementação de rotação FIFO e emissão diária do auto de pesagem de avarias.',
                'ordem': 3,
                'itens': [
                    ('Pesagem formal matinal de fruta avariada antes do descarte', 'Proibido descartar qualquer fruta ou legume sem pesagem prévia na balança de serviço e registo de código.', 'Quebra oculta sem reflexo contabilístico no CMVC.', 'conforme', 'Diária (08h00)'),
                    ('Rotação de produto pelo método FIFO (Primeiro que entra, primeiro que sai)', 'Colocar a mercadoria nova no fundo ou por baixo dos produtos já expostos e maturados.', 'Aceleração de quebra por envelhecimento no expositor.', 'conforme', 'Contínua'),
                    ('Criação de sacos promocionais de escoamento para fruta madura', 'Embalar fruta com aspeto maduro mas próprio para consumo a 50% do PVP para consumo rápido ou sopas.', 'Recuperação de 60% a 70% do custo de aquisição da fruta.', 'conforme', 'Diária (14h00)'),
                    ('Limpeza e pulverização de bancadas de folhas verdes', 'Higienização diária e manutenção de humidade para alfaces, couves e ervas aromáticas.', 'Perda de peso por dessecação e quebra visual.', 'conforme', 'Diária')
                ]
            },
            {
                'nome': 'Linha de Caixas & Ponto de Venda (POS)',
                'icone': 'credit-card',
                'responsavel_padrao': 'Supervisora de Caixas',
                'descricao': 'Auditoria ao ponto nevrálgico de cobrança e saída de mercadoria. Eliminação de erros de leitura de códigos de barras e controlo de fechos de caixa.',
                'ordem': 4,
                'itens': [
                    ('Conferência cega de fundo de maneio e fecho de turno de caixa', 'O operador conta o numerário sem saber o valor registado no sistema de faturação.', 'Risco de quebras de caixa encobertas e desvios de numerário.', 'conforme', 'Por turno'),
                    ('Validação de leitura de código de barras unitário vs. Pack/Grade', 'Garantir que grades de cerveja ou packs de leite não são registados pelo código de unidade com preço simples.', 'Prejuízo brutal de 70% a 80% do valor da mercadoria no ato da venda.', 'conforme', 'Amostragem diária'),
                    ('Controlo de artigos sem leitura ótica (Entrada manual de código)', 'Auditar talões com excesso de digitação manual de PLUs e códigos de barra danificados.', 'Troca voluntária ou involuntária de códigos caros por baratos.', 'em_correcao', 'Semanal'),
                    ('Aferição da taxa de IVA atribuída nos artigos de impulso no checkout', 'Verificar se gomas, chocolates e pilhas estão com IVA a 23% e não a 6%.', 'Prejuízo fiscal com autuação pelas Finanças.', 'conforme', 'Mensal')
                ]
            }
        ]

        for a_idx, a_data in enumerate(areas_data, 1):
            area, _ = AreaVerificacao.objects.update_or_create(
                nome=a_data['nome'],
                defaults={
                    'icone': a_data['icone'],
                    'responsavel_padrao': a_data['responsavel_padrao'],
                    'descricao': a_data['descricao'],
                    'ordem': a_idx
                }
            )
            for ponto, pop, risco, status, freq in a_data['itens']:
                ChecklistItem.objects.update_or_create(
                    area=area,
                    ponto_verificacao=ponto,
                    defaults={
                        'procedimento_padrao': pop,
                        'risco_financeiro': risco,
                        'status': status,
                        'frequencia': freq,
                    }
                )

        # 9. Documentos & Minutas de Consultoria
        documentos_data = [
            {
                'categoria': 'minutas',
                'codigo': 'MIN-AT-CIVA-86',
                'titulo': 'Minuta Oficial de Auto de Abate e Destruição de Quebras (Art.º 86.º CIVA)',
                'formato': 'PDF / Word (.docx)',
                'enquadramento_legal': 'Artigo 86.º n.º 1 e 2 do Código do IVA / Artigo 23.º do Código do IRC',
                'descricao': 'Minuta jurídica e fiscal obrigatória para regularização de quebras e perecimento perante a Autoridade Tributária. Permite a dedução fiscal do custo das mercadorias sem liquidação de IVA compensatório.',
                'conteudo_minuta': """REINO DE PORTUGAL / AUTORIDADE TRIBUTÁRIA E ADUANEIRA
AUTO DE ABATE E DESTRUIÇÃO DE MERCADORIAS POR PERECIMENTO OU OBSOLESCÊNCIA
(Nos termos e para os efeitos do disposto no n.º 1 do artigo 86.º do Código do IVA e alínea d) do n.º 1 do artigo 23.º do Código do IRC)

Aos [DATA], nas instalações da sociedade [FIRMA], NIF [NIF], sita em [MORADA], procedeu-se à verificação, inutilização e abate físico de mercadorias deterioradas sem qualquer valor comercial residual.

1. DESCRIÇÃO DAS MERCADORIAS ABATIDAS:
- Secção de Frescos (Talho/Quebra de Desmanche): [VALOR_TALHO] €
- Secção de Frutas e Legumes (Perecimento Natural): [VALOR_FLV] €
- Secção de Lacticínios e Charcutaria (Validade Expirada): [VALOR_CHARC] €
VALOR TOTAL DO CMVC ABATIDO: [TOTAL] €

2. DECLARAÇÃO DE TESTEMUNHAS E RESPONSÁVEIS:
Os signatários declaram sob compromisso de honra que os bens supramencionados foram devidamente inutilizados para consumo humano e encaminhados para o operador licenciado de gestão de resíduos / subprodutos animais (DGV), não existindo qualquer proveito económico da sua alienação.

Assinatura do Sócio-Gerente: ___________________________________________
Assinatura do Responsável Técnico: ____________________________________
Assinatura do Contabilista Certificado (CC n.º _____): ___________________"""
            },
            {
                'categoria': 'fichas_tecnicas',
                'codigo': 'FT-DESMANCHE-BOV-01',
                'titulo': 'Ficha Técnica Padrão de Desmanche de Novilho Nacional (Quarto Traseiro e Dianteiro)',
                'formato': 'Excel (.xlsx) / PDF',
                'enquadramento_legal': 'Controlo de Margem Bruta e Fórmulas de Formação de PVP no Retalho',
                'descricao': 'Planilha paramétrica que calcula o fator de desmanche, o rendimento em carne limpa vendável e o PVP mínimo necessário por corte (Lombo, Vazia, Alcatra, Aba e Pedaços) para atingir 28% de margem líquida.',
                'conteudo_minuta': """FICHA TÉCNICA DE DESMANCHE DE CARNE DE BOVINO / NOVILHO
PESO BRUTO ENTRADA: 100,0 kg | CUSTO FATURA: 6,20 €/kg | VALOR LOTE: 620,00 €

RENDIMENTO REAL AUDITADO:
- Carnes de 1.ª (Lombo, Vazia, Alcatra, Chã): 38,0 kg (38,0%) -> PVP Médio: 14,90 €/kg
- Carnes de 2.ª (Acém, Pojadouro, Pá): 24,0 kg (24,0%) -> PVP Médio: 9,80 €/kg
- Carnes de 3.ª e Preparados (Aba, Cachaço, Aparas): 14,0 kg (14,0%) -> PVP Médio: 6,40 €/kg
- Quebra Técnica (Ossos e Sebo Desprovido de Valor): 24,0 kg (24,0%) -> PVP: 0,00 €/kg

CUSTO REAL DO KG LIMPO VENDÁVEL: 620,00 € / 76,0 kg = 8,16 €/kg
(Se calcular o preço sobre o custo da fatura de 6,20 €, a loja perde 1,96 € em cada quilo vendido!)"""
            },
            {
                'categoria': 'pops',
                'codigo': 'POP-CAIS-RECECAO-01',
                'titulo': 'Procedimento Operacional Padrão: Protocolo de Receção Cega no Cais de Cargas',
                'formato': 'PDF Normativo',
                'enquadramento_legal': 'Norma ISO 22000 / Boas Práticas de Retalho e Controlo de Perdas',
                'descricao': 'Manual de instrução de trabalho para encarregados de armazém. Estabelece a proibição de carimbos prévios em guias de remessa e o roteiro de pesagem obrigatória.',
                'conteudo_minuta': """PROCEDIMENTO OPERACIONAL PADRONIZADO: RECEÇÃO CEGA NO CAIS
OBJETIVO: Eliminar faturas com divergência de quantidade e preços em relação ao acordado.

PASSO 1: O motorista entrega apenas a Guia de Transporte. A Fatura Comercial com preços fica retida na cabine ou envelope fechado.
PASSO 2: O operador conta todas as caixas fisicamente e anota numa folha em branco (Conferência Cega).
PASSO 3: Nos frescos, cada palete ou gancho é obrigatoriamente passado na balança calibrada de plataforma.
PASSO 4: Se o peso apurado for inferior em mais de 1,5% ao declarado na guia, emite-se Albará de Rejeição Parcial de imediato.
PASSO 5: Apenas após a contagem física o encarregado confere o sistema informático e valida o documento de transporte."""
            },
            {
                'categoria': 'escalas',
                'codigo': 'MATRIZ-ESCALAS-RETALHO',
                'titulo': 'Matriz de Dimensionamento de Escalas Horárias por Curva de Tráfego de Clientes',
                'formato': 'Excel Paramétrico',
                'enquadramento_legal': 'Código do Trabalho Português / Organização dos Tempos de Trabalho',
                'descricao': 'Ferramenta de cálculo para distribuir operadores de caixa e repositores em função do número de talões emitidos por hora no POS, erradicando filas no pico e ociosidade de manhã.',
                'conteudo_minuta': """MATRIZ DE ESCALAS POR FLUXO HORÁRIO DE CLIENTES (ETPOS/WINREST)
RÁCIO BENCHMARK: 1 Operador de Caixa para cada 24 talões/hora.

HORÁRIOS AUDITADOS NO SUPERMERCADO:
- 08h30 às 11h30 (Manhã Útil): Média de 14 talões/hora -> Necessidade: 1 Caixa aberta (+ reposição leve).
- 12h00 às 14h00 (Almoço): Média de 32 talões/hora -> Necessidade: 2 Caixas abertas.
- 15h00 às 17h00 (Tarde Baixa): Média de 18 talões/hora -> Necessidade: 1 Caixa aberta.
- 17h30 às 19h45 (Pico Regresso ao Lar): Média de 65 talões/hora -> Necessidade: 3 Caixas em pleno funcionamento!

DESVIO DETETADO: A loja mantinha 3 caixas abertas de manhã (excesso de 2 operadores) e apenas 2 caixas abertas no pico das 18h30 (filas de 12 minutos e desistência de compras)."""
            }
        ]

        for doc in documentos_data:
            DocumentoConsultoria.objects.update_or_create(codigo=doc['codigo'], defaults=doc)

        self.stdout.write(self.style.SUCCESS('Plataforma Vértice Retalho Portugal: Base de Dados Nacional Atualizada com Sucesso!'))
