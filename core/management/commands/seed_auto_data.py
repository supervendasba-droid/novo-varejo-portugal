from django.core.management.base import BaseCommand
from core.models import (
    EmpresaAutomovel, ViaturaStand, OrdemOficina, SegmentoRentACar, AlertaAutomovel
)

class Command(BaseCommand):
    help = 'Povoa a base de dados com indicadores de consultoria para o Setor Automóvel (Stand + Oficina + Rent-a-Car)'

    def handle(self, *args, **options):
        self.stdout.write("A povoar dados de Consultoria Automóvel em Portugal...")

        # 1. Empresa Concessão Integrada
        empresa, _ = EmpresaAutomovel.objects.get_or_create(
            nif='509881223',
            defaults={
                'nome': 'AutoVila Motors & Rent Lda.',
                'razao_social': 'AutoVila Comércio, Manutenção e Aluguer de Veículos Lda.',
                'localizacao': 'Leiria (Zona Industrial Sul • IC2)',
                'num_viaturas_frota': 48,
                'num_elevadores_oficina': 6,
                'num_carros_stand': 35,
                'faturacao_mensal_global': 380000.00,
                'faturacao_stand': 220000.00,
                'faturacao_oficina': 95000.00,
                'faturacao_rentacar': 65000.00,
                'fuga_mensal_mapeada': 14800.00,
            }
        )

        # 2. Viaturas Stand (Aging, Custo de Chão de Fábrica e Regime da Margem)
        ViaturaStand.objects.all().delete()
        viaturas_dados = [
            {
                'matricula': 'AA-42-ZZ',
                'viatura': 'Mercedes-Benz Classe A 180 d AMG Line Auto',
                'ano': 2021,
                'kms': 68500,
                'dias_em_stock': 118,
                'custo_aquisicao': 21800.00,
                'custo_recondicionamento': 850.00,
                'custo_financeiro_parado': 520.00,
                'pvp_anunciado': 24900.00,
                'pvp_desagio_sugerido': 23750.00,
                'regime_iva': 'Regime da Margem (DL 199/96)',
                'desagio_aplicado': False
            },
            {
                'matricula': '48-XF-12',
                'viatura': 'BMW Série 3 Touring 320d Pack M Auto',
                'ano': 2020,
                'kms': 92000,
                'dias_em_stock': 94,
                'custo_aquisicao': 25500.00,
                'custo_recondicionamento': 1100.00,
                'custo_financeiro_parado': 490.00,
                'pvp_anunciado': 29400.00,
                'pvp_desagio_sugerido': 27900.00,
                'regime_iva': 'Regime da Margem (DL 199/96)',
                'desagio_aplicado': False
            },
            {
                'matricula': 'BH-89-TA',
                'viatura': 'Renault Clio V 1.0 TCe RS Line',
                'ano': 2022,
                'kms': 41200,
                'dias_em_stock': 78,
                'custo_aquisicao': 13200.00,
                'custo_recondicionamento': 420.00,
                'custo_financeiro_parado': 260.00,
                'pvp_anunciado': 15800.00,
                'pvp_desagio_sugerido': 14950.00,
                'regime_iva': 'Regime da Margem (DL 199/96)',
                'desagio_aplicado': False
            },
            {
                'matricula': 'AJ-15-OP',
                'viatura': 'Peugeot 3008 1.5 BlueHDi Allure EAT8',
                'ano': 2021,
                'kms': 74000,
                'dias_em_stock': 85,
                'custo_aquisicao': 20400.00,
                'custo_recondicionamento': 780.00,
                'custo_financeiro_parado': 410.00,
                'pvp_anunciado': 23900.00,
                'pvp_desagio_sugerido': 22800.00,
                'regime_iva': 'Regime da Margem (DL 199/96)',
                'desagio_aplicado': False
            },
            {
                'matricula': '62-VM-88',
                'viatura': 'Volkswagen Golf 2.0 TDI Life DSG',
                'ano': 2021,
                'kms': 58000,
                'dias_em_stock': 42,
                'custo_aquisicao': 19800.00,
                'custo_recondicionamento': 550.00,
                'custo_financeiro_parado': 210.00,
                'pvp_anunciado': 22900.00,
                'pvp_desagio_sugerido': 22300.00,
                'regime_iva': 'Regime da Margem (DL 199/96)',
                'desagio_aplicado': True
            },
            {
                'matricula': 'AR-99-BC',
                'viatura': 'Nissan Qashqai 1.3 DIG-T N-Connecta',
                'ano': 2022,
                'kms': 34000,
                'dias_em_stock': 28,
                'custo_aquisicao': 18500.00,
                'custo_recondicionamento': 390.00,
                'custo_financeiro_parado': 130.00,
                'pvp_anunciado': 21900.00,
                'pvp_desagio_sugerido': 21400.00,
                'regime_iva': 'Regime Geral IVA 23%',
                'desagio_aplicado': False
            },
            {
                'matricula': '09-TF-44',
                'viatura': 'Fiat 500 1.0 Hybrid Dolcevita',
                'ano': 2023,
                'kms': 19500,
                'dias_em_stock': 19,
                'custo_aquisicao': 11400.00,
                'custo_recondicionamento': 250.00,
                'custo_financeiro_parado': 65.00,
                'pvp_anunciado': 13800.00,
                'pvp_desagio_sugerido': 13500.00,
                'regime_iva': 'Regime da Margem (DL 199/96)',
                'desagio_aplicado': False
            },
            {
                'matricula': 'BK-33-LM',
                'viatura': 'Toyota Yaris 1.5 Hybrid Comfort',
                'ano': 2022,
                'kms': 47000,
                'dias_em_stock': 22,
                'custo_aquisicao': 14900.00,
                'custo_recondicionamento': 310.00,
                'custo_financeiro_parado': 95.00,
                'pvp_anunciado': 17600.00,
                'pvp_desagio_sugerido': 17200.00,
                'regime_iva': 'Regime da Margem (DL 199/96)',
                'desagio_aplicado': False
            }
        ]
        for v in viaturas_dados:
            ViaturaStand.objects.create(**v)

        # 3. Ordens de Oficina (Eficiência Mão de Obra e Margem de Peças)
        OrdemOficina.objects.all().delete()
        oficina_dados = [
            {
                'numero_or': 'OR-2026-104',
                'cliente': 'TransTejo Logística Lda.',
                'viatura': 'Renault Master 2.3 dCi 145 Furgão',
                'tipo_servico': 'Kit Distribuição + Bomba de Água + Revisão 120k',
                'horas_orcamentadas': 5.5,
                'horas_faturadas': 4.0,
                'valor_mao_obra': 180.00,
                'custo_pecas_grossista': 340.00,
                'pvp_pecas_faturado': 430.00,
                'perda_margem_pecas': 75.00
            },
            {
                'numero_or': 'OR-2026-105',
                'cliente': 'Eng.º Miguel Silvestre (Particular)',
                'viatura': 'Audi A4 Avant 2.0 TDI S-Tronic',
                'tipo_servico': 'Pastilhas + Discos Dianteiros/Traseiros Brembo',
                'horas_orcamentadas': 2.5,
                'horas_faturadas': 1.8,
                'valor_mao_obra': 81.00,
                'custo_pecas_grossista': 260.00,
                'pvp_pecas_faturado': 335.00,
                'perda_margem_pecas': 52.00
            },
            {
                'numero_or': 'OR-2026-106',
                'cliente': 'Frota Rent-a-Car Interna (Viatura 14)',
                'viatura': 'Peugeot 208 1.2 PureTech',
                'tipo_servico': 'Revisão 40.000 km + Troca Óleo 0W20 + Filtros',
                'horas_orcamentadas': 1.8,
                'horas_faturadas': 1.8,
                'valor_mao_obra': 81.00,
                'custo_pecas_grossista': 75.00,
                'pvp_pecas_faturado': 125.00,
                'perda_margem_pecas': 0.00
            },
            {
                'numero_or': 'OR-2026-107',
                'cliente': 'Dr.ª Carla Figueiredo (Seguradora Fidelidade)',
                'viatura': 'Mercedes-Benz CLA 200 Shooting Brake',
                'tipo_servico': 'Diagnóstico Eletrónico AdBlue + Sensor NOX',
                'horas_orcamentadas': 3.0,
                'horas_faturadas': 2.0,
                'valor_mao_obra': 90.00,
                'custo_pecas_grossista': 410.00,
                'pvp_pecas_faturado': 480.00,
                'perda_margem_pecas': 95.00
            },
            {
                'numero_or': 'OR-2026-108',
                'cliente': 'Construções Leirienses SA',
                'viatura': 'Toyota Hilux 2.4 D-4D 4x4',
                'tipo_servico': 'Embraiagem Reforçada + Valvolina Caixa/Diferencial',
                'horas_orcamentadas': 6.0,
                'horas_faturadas': 4.5,
                'valor_mao_obra': 202.50,
                'custo_pecas_grossista': 520.00,
                'pvp_pecas_faturado': 660.00,
                'perda_margem_pecas': 110.00
            }
        ]
        for o in oficina_dados:
            OrdemOficina.objects.create(**o)

        # 4. Segmentos Rent-a-Car (Ocupação, RevPAV e Ponto de Desmobilização)
        SegmentoRentACar.objects.all().delete()
        rent_dados = [
            {
                'categoria': 'Grupo B - Compacto Utilitário',
                'viaturas_exemplo': 'Renault Clio / Peugeot 208 / Seat Ibiza',
                'qtd_viaturas': 18,
                'taxa_ocupacao_atual': 71.0,
                'taxa_ocupacao_alvo': 85.0,
                'diaria_media': 38.00,
                'revpav_atual': 26.98,
                'revpav_alvo': 32.30,
                'custo_km': 0.118,
                'dias_para_desmobilizacao': 60,
                'tributacao_autonoma': '10% (Valor aquisição < 27.500 €)'
            },
            {
                'categoria': 'Grupo C - SUV Urbano & Crossover',
                'viaturas_exemplo': 'Nissan Juke / Peugeot 2008 / Renault Captur',
                'qtd_viaturas': 14,
                'taxa_ocupacao_atual': 64.0,
                'taxa_ocupacao_alvo': 82.0,
                'diaria_media': 52.00,
                'revpav_atual': 33.28,
                'revpav_alvo': 42.64,
                'custo_km': 0.142,
                'dias_para_desmobilizacao': 45,
                'tributacao_autonoma': '10% (Valor aquisição < 27.500 €)'
            },
            {
                'categoria': 'Grupo F - Furgões Comerciais Ligeiros',
                'viaturas_exemplo': 'Renault Master / Citroën Berlingo / Ford Transit',
                'qtd_viaturas': 10,
                'taxa_ocupacao_atual': 79.0,
                'taxa_ocupacao_alvo': 88.0,
                'diaria_media': 58.00,
                'revpav_atual': 45.82,
                'revpav_alvo': 51.04,
                'custo_km': 0.155,
                'dias_para_desmobilizacao': 120,
                'tributacao_autonoma': '0% Isento (Ligeiro de Mercadorias Art.º 88.º CIRC)'
            },
            {
                'categoria': 'Grupo E - 100% Elétrico Urbano (EV)',
                'viaturas_exemplo': 'Peugeot e-208 / Fiat 500e / Renault Zoe',
                'qtd_viaturas': 6,
                'taxa_ocupacao_atual': 58.0,
                'taxa_ocupacao_alvo': 80.0,
                'diaria_media': 48.00,
                'revpav_atual': 27.84,
                'revpav_alvo': 38.40,
                'custo_km': 0.082,
                'dias_para_desmobilizacao': 90,
                'tributacao_autonoma': '0% Isento (Veículo 100% Elétrico CIRC)'
            }
        ]
        for r in rent_dados:
            SegmentoRentACar.objects.create(**r)

        # 5. Alertas de Gestão Automóvel
        AlertaAutomovel.objects.all().delete()
        alertas_dados = [
            {
                'setor': 'stand',
                'titulo': '4 Viaturas na "Curva C" com Mais de 75 Dias no Pátio',
                'descricao': 'Capital imobilizado de 80.900 € a incorrer em 1.680 €/mês de juros de chão de fábrica (Floor Plan). Recomendado deságio promocional de 3% a 5% para libertação imediata de tesouraria.',
                'impacto_euros': 6200.00,
                'criticidade': 'alta',
                'resolvido': False
            },
            {
                'setor': 'oficina',
                'titulo': 'Perda de Eficiência em Mão de Obra: 1,2 Horas Perdidas por OR',
                'descricao': 'Cruzamento entre horas apontadas em oficina e horas faturadas no SAF-T revela que 24% do tempo dos mecânicos não é cobrado aos clientes ou orçamentos de seguradora.',
                'impacto_euros': 5100.00,
                'criticidade': 'alta',
                'resolvido': False
            },
            {
                'setor': 'rentacar',
                'titulo': 'Subutilização de Frota nos Grupos B e C (Ocupação a 67% vs Meta 84%)',
                'descricao': 'Desfasamento de tarifas dinâmicas nas plataformas de reserva (brokers). Ajuste de pricing diário gerará mais 3.500 €/mês sem custos adicionais de frota.',
                'impacto_euros': 3500.00,
                'criticidade': 'alta',
                'resolvido': False
            },
            {
                'setor': 'fiscal',
                'titulo': 'Incongruência no Regime da Margem de IVA (DL n.º 199/96)',
                'descricao': '2 viaturas com retoma de particulares foram faturadas com IVA liquidado sobre a totalidade e não sobre a margem de revenda, gerando pagamento indevido de IVA à AT.',
                'impacto_euros': 2400.00,
                'criticidade': 'media',
                'resolvido': False
            }
        ]
        for a in alertas_dados:
            AlertaAutomovel.objects.create(**a)

        self.stdout.write(self.style.SUCCESS("Dados de Consultoria Automóvel gerados com sucesso!"))
