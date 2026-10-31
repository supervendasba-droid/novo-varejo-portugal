from django.core.management.base import BaseCommand
from core.models import (
    Supermercado, AlavancaVenda, PlanoAcaoOperacional,
    LayoutSupermercadoItem, RedeSetorialRanking, PortalClienteToken, OportunidadeIndustria
)
import uuid

class Command(BaseCommand):
    help = 'Povoa a base de dados com a metodologia completa do Ecossistema Novo Varejo (Alavancas, Planos de Ação, Layout, Rankings e Indústria)'

    def handle(self, *args, **options):
        self.stdout.write("A povoar dados do Ecossistema Novo Varejo...")
        supermercado = Supermercado.objects.first()

        # 1. Alavanca da Venda (A Fórmula do Resultado)
        AlavancaVenda.objects.all().delete()
        AlavancaVenda.objects.create(
            supermercado=supermercado,
            mes_referencia='Março 2026',
            venda_total=120000.00,
            num_clientes_fluxo=8450,
            itens_por_talao=6.80,
            valor_medio_item=2.08,
            ticket_medio=14.20,
            alavanca_ofensora='fluxo',
            variacao_fluxo_pct=-8.0,
            variacao_ticket_pct=+3.2,
            diagnostico_causa='A quebra de faturação não decorre do cesto de compras (ticket médio subiu 3,2%), mas sim da perda de 735 clientes no mês (-8%). A evasão concentra-se no horário pós-laboral (17h30 às 20h00) motivada pela rutura de pão quente na padaria e desabastecimento no linear de frescos e FLV.',
            meta_fluxo=9200,
            meta_itens_talao=7.50,
            meta_valor_item=2.15
        )

        # 2. Planos de Ação Operacionais (Da Estratégia ao Chão de Loja)
        PlanoAcaoOperacional.objects.all().delete()
        planos = [
            {
                'supermercado': supermercado,
                'problema': 'Falta de pão quente após as 17h30 afasta clientes habituais de regresso a casa',
                'prioridade': 'P1',
                'acao': 'Programar fornadas automáticas às 17h00 e 18h30 com aviso sonoro em loja e degustação de broa',
                'responsavel': 'Chefe de Secção Padaria (Manuel Ribeiro)',
                'prazo_dias': 3,
                'acompanhamento': 'Registo diário de sobras e horas de cozedura no fecho de turno',
                'status': 'em_execucao',
                'resultado_esperado': '+1.400 € / mês recuperados em venda casada de padaria e café',
                'resultado_medido': '+1.520 € / mês medido no SAF-T'
            },
            {
                'supermercado': supermercado,
                'problema': 'Ruturas de linear de frutas e legumes no final da tarde por falta de reposição',
                'prioridade': 'P1',
                'acao': 'Criar rotina de reposição e pulverização obrigatória às 16h30 com triagem de produtos maduros',
                'responsavel': 'Responsável FLV (Sílvia Carmo)',
                'prazo_dias': 2,
                'acompanhamento': 'Auditoria fotográfica diária às 17h00 antes do pico de clientes',
                'status': 'em_execucao',
                'resultado_esperado': '+1.800 € / mês em vendas de frescos',
                'resultado_medido': '+1.750 € / mês recuperados'
            },
            {
                'supermercado': supermercado,
                'problema': 'Erosão de margem em 142 artigos Curva A por desfasamento de tabelas de grossistas',
                'prioridade': 'P2',
                'acao': 'Importação da tabela de preços atualizada no software POS (ETPOS) e emissão de novas etiquetas de prateleira',
                'responsavel': 'Consultor Regis Costa / Operador de Caixa Central',
                'prazo_dias': 5,
                'acompanhamento': 'Conferência aleatória de 20 etiquetas por linear com leitor ótico',
                'status': 'concluido',
                'resultado_esperado': '+1.850 € / mês de margem bruta estancada',
                'resultado_medido': '+1.850 € / mês plenamente recuperados'
            },
            {
                'supermercado': supermercado,
                'problema': 'Quebras não documentadas no talho geram distorções no CMVC e balancete analítico',
                'prioridade': 'P2',
                'acao': 'Implementação da ficha técnica de desmanche de novilho e parametrização de autos formais do Art.º 86.º CIVA',
                'responsavel': 'Mestre Talhante (António Silva) & Contabilista Certificado',
                'prazo_dias': 7,
                'acompanhamento': 'Pesagem obrigatória de osso e sebo em tara dedicada antes de descarte',
                'status': 'em_execucao',
                'resultado_esperado': '+2.400 € / mês em margem e proteção fiscal',
                'resultado_medido': 'Em auditoria no fecho do mês'
            }
        ]
        for p in planos:
            PlanoAcaoOperacional.objects.create(**p)

        # 3. Layout de Supermercado & Merchandising
        LayoutSupermercadoItem.objects.all().delete()
        layouts = [
            {
                'zona': 'entrada',
                'titulo': 'Zona de Descompressão & Frutas e Legumes (FLV)',
                'conceito_fluxo': 'O cliente entra e necessita de 3 a 5 passos para desacelerar o ritmo da rua. A secção de FLV na entrada transmite frescura, cor e abundância, estimulando o apetite e a perceção de preço justo logo no primeiro contacto.',
                'estrategia_exposicao': 'Bancas baixas em ilha para garantir visibilidade total da loja. Exposição em pirâmide de frutas da época (maçãs de Alcobaça, laranjas do Algarve) com contrastes visuais de cor.',
                'impacto_venda': '+12% de conversão na entrada de loja',
                'icone': 'apple'
            },
            {
                'zona': 'central',
                'titulo': 'Corredores Centrais: Mercearia & Planograma por Categoria',
                'conceito_fluxo': 'Os corredores centrais concentram a mercearia seca e produtos de compra rotineira (arroz, massas, azeites). O fluxo deve ser amplo para permitir a passagem simultânea de dois carrinhos de compras.',
                'estrategia_exposicao': 'Organização vertical por marcas: produtos de maior margem colocados ao nível dos olhos (1,40m a 1,60m) e artigos pesados ou básicos na base da gôndola.',
                'impacto_venda': '+9% no volume médio de artigos por cesto',
                'icone': 'shopping-bag'
            },
            {
                'zona': 'fundo',
                'titulo': 'Fundo da Loja: Secções de Destino Obrigatório (Talho & Padaria)',
                'conceito_fluxo': 'O pão fresco e a carne são os maiores geradores de visita ao supermercado. Colocá-los no fundo da loja obriga o cliente a percorrer os corredores centrais, aumentando a probabilidade de compras por impulso.',
                'estrategia_exposicao': 'Balcão de atendimento tradicional com vitrine iluminada e cheiro ativo de pão acabado de cozer. Iluminação quente (3000K) no talho para realçar o vermelho natural da carne.',
                'impacto_venda': '+18% de circulação em toda a área de venda',
                'icone': 'flame'
            },
            {
                'zona': 'checkouts',
                'titulo': 'Linha de Caixas: O Ponto Quente de Compras por Impulso',
                'conceito_fluxo': 'Enquanto aguarda na fila de pagamento, o consumidor está vulnerável a microdecisões de gratificação pessoal (doces, snacks, pilhas, revistas).',
                'estrategia_exposicao': 'Expositores compactos colados à passadeira de caixa com artigos de valor inferior a 1,50 € (pastilhas Trident, chocolates, pilhas AA e pequenos desinfetantes).',
                'impacto_venda': '+1,10 € de incremento no ticket médio por cliente',
                'icone': 'credit-card'
            }
        ]
        for l in layouts:
            LayoutSupermercadoItem.objects.create(**l)

        # 4. Rankings de Inteligência Setorial (Terminal do Analista - Portugal)
        RedeSetorialRanking.objects.all().delete()
        rankings = [
            {
                'posicao': 1,
                'grupo_insignia': 'Continente (Sonae MC)',
                'sede_pais': 'Portugal (Matosinhos)',
                'faturacao_anual_milhoes': 4350.0,
                'num_lojas': 560,
                'quota_mercado_pct': 28.4,
                'venda_m2_ano': 5600,
                'tendencia_estrategica': 'Liderança consolidada com forte aposta em proximidade (Continente Bom Dia) e fidelização Cartão Continente.',
                'arquetipo_operacao': 'Hipermercados & Supermercados Urbanos'
            },
            {
                'posicao': 2,
                'grupo_insignia': 'Pingo Doce (Jerónimo Martins)',
                'sede_pais': 'Portugal (Lisboa)',
                'faturacao_anual_milhoes': 4120.0,
                'num_lojas': 475,
                'quota_mercado_pct': 26.9,
                'venda_m2_ano': 6100,
                'tendencia_estrategica': 'Destaque absoluto em perecíveis frescos, marca própria e expansão contínua do conceito de comida pronta / restauração.',
                'arquetipo_operacao': 'Supermercados de Proximidade & FLV'
            },
            {
                'posicao': 3,
                'grupo_insignia': 'Lidl Portugal',
                'sede_pais': 'Alemanha (Sintra/Portugal)',
                'faturacao_anual_milhoes': 2180.0,
                'num_lojas': 275,
                'quota_mercado_pct': 14.2,
                'venda_m2_ano': 6800,
                'tendencia_estrategica': 'Modelo de discount inteligente com padaria quente de alto giro e modernização de lojas para formatos ecológicos.',
                'arquetipo_operacao': 'Smart Discounter de Grande Superfície'
            },
            {
                'posicao': 4,
                'grupo_insignia': 'Intermarché (Os Mosqueteiros)',
                'sede_pais': 'França / Independentes PT',
                'faturacao_anual_milhoes': 1620.0,
                'num_lojas': 260,
                'quota_mercado_pct': 10.6,
                'venda_m2_ano': 4400,
                'tendencia_estrategica': 'Rede de franchisados e empresários independentes com forte implantação regional no interior e postos de combustível.',
                'arquetipo_operacao': 'Supermercado Independente com Posto de Abastecimento'
            },
            {
                'posicao': 5,
                'grupo_insignia': 'Auchan Retail Portugal',
                'sede_pais': 'França (Carnaxide/Portugal)',
                'faturacao_anual_milhoes': 980.0,
                'num_lojas': 78,
                'quota_mercado_pct': 6.4,
                'venda_m2_ano': 4900,
                'tendencia_estrategica': 'Transição para formatos de hipermercado compacto e aquisição recente dos supermercados Minipreço/Dia em Portugal.',
                'arquetipo_operacao': 'Hipermercados & Supermercados My Auchan'
            },
            {
                'posicao': 6,
                'grupo_insignia': 'Mercadona Portugal',
                'sede_pais': 'Espanha (Vila Nova de Gaia)',
                'faturacao_anual_milhoes': 890.0,
                'num_lojas': 49,
                'quota_mercado_pct': 5.8,
                'venda_m2_ano': 7400,
                'tendencia_estrategica': 'A rede com maior crescimento e maior faturação média por metro quadrado em Portugal. Estratégia SPB (Sempre Preços Baixos).',
                'arquetipo_operacao': 'Supermercado Modelo de Grande Eficiência'
            },
            {
                'posicao': 7,
                'grupo_insignia': 'Coviran Portugal',
                'sede_pais': 'Espanha / Portugal (Sintra)',
                'faturacao_anual_milhoes': 240.0,
                'num_lojas': 290,
                'quota_mercado_pct': 1.6,
                'venda_m2_ano': 3800,
                'tendencia_estrategica': 'Cooperativa de retalhistas de aldeia e bairros urbanos, assegurando proximidade comunitária.',
                'arquetipo_operacao': 'Mercearias e Minimercados de Bairro'
            },
            {
                'posicao': 8,
                'grupo_insignia': 'Meu Super (Sonae MC)',
                'sede_pais': 'Portugal',
                'faturacao_anual_milhoes': 190.0,
                'num_lojas': 315,
                'quota_mercado_pct': 1.2,
                'venda_m2_ano': 3950,
                'tendencia_estrategica': 'Franchising de proximidade sem royalties diretos, alavancando a gama e logística Continente.',
                'arquetipo_operacao': 'Franchising de Loja de Conveniência'
            }
        ]
        for r in rankings:
            RedeSetorialRanking.objects.create(**r)

        # 5. Token Seguro para o Portal do Cliente
        PortalClienteToken.objects.all().delete()
        token_fixo = uuid.UUID('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d')
        PortalClienteToken.objects.create(
            token=token_fixo,
            supermercado=supermercado,
            destinatario_nome='Carlos Manuel Ferraz (Sócio-Gerente)',
            destinatario_email='gerencia@supermercadodavila.pt',
            permissoes='bi_dashboards,planos_acao,lancamento_diario',
            ativo=True,
            visualizacoes=14
        )

        # 6. Oportunidades Comerciais (Portal da Indústria & Distribuição)
        OportunidadeIndustria.objects.all().delete()
        oportunidades = [
            {
                'categoria': 'Lacticínios & Queijos Tradicionais',
                'marca_parceira': 'Lactogal / Mimosa & Matinal',
                'regiao_oportunidade': 'Norte e Centro (Porto, Braga, Leiria)',
                'diagnostico_gondola': 'Rutura de linear de 14,2% verificada aos sábados à tarde nos leites enriquecidos e queijo fatiado flamengo. Oportunidade de rever frequência de entrega para bi-semanal.',
                'potencial_sellout_euros': 8500.00,
                'taxa_rutura_linear': 14.2
            },
            {
                'categoria': 'Azeites Virgem Extra & Óleos',
                'marca_parceira': 'Sovena / Oliveira da Serra',
                'regiao_oportunidade': 'Grande Lisboa & Vale do Tejo',
                'diagnostico_gondola': 'Desfasamento de PVP de 0,45 €/garrafa face ao hipermercado vizinho reduz volume de venda. Promoção cruzada com bacalhau na Páscoa pode alavancar +35% de vendas.',
                'potencial_sellout_euros': 6200.00,
                'taxa_rutura_linear': 8.5
            },
            {
                'categoria': 'Cervejas Nacionais & Artesanais',
                'marca_parceira': 'Super Bock Group',
                'regiao_oportunidade': 'Algarve & Litoral Alentejano',
                'diagnostico_gondola': 'Elevada procura sazonal de packs de 24 garrafas sem espaço de gôndola suficiente. Instalação de topo de gôndola refrigerado gera conversão imediata.',
                'potencial_sellout_euros': 9400.00,
                'taxa_rutura_linear': 16.0
            }
        ]
        for o in oportunidades:
            OportunidadeIndustria.objects.create(**o)

        self.stdout.write(self.style.SUCCESS("Dados do Ecossistema Novo Varejo gerados com sucesso!"))
