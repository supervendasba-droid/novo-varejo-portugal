# Novo Varejo Inteligência de Mercado | Regis Costa Consultoria (Python Django)

Plataforma Web de Elite e SPA Institucional para Consultoria Empresarial Especializada em **Retalho Alimentar e Supermercados de Proximidade em Portugal**.

---

## 🇵🇹 Normas e Terminologia de Portugal (PT-PT)

A aplicação segue rigorosamente as normas tributárias, comerciais e a terminologia corporativa do retalho em Portugal:
- **Terminologia:** Faturação, tesouraria, avença mensal, rotura de stock, talho, charcutaria, FLV (frutas, legumes e verduras), PVP, contabilidade analítica, sócio-gerente, cais de receção, albará/guia de remessa, concelho, telemóvel.
- **Enquadramento Legal e Fiscal:**
  - Ficheiro **SAF-T (PT)** (Portaria n.º 302/2016 e estrutura tributária da AT).
  - **Artigo 86.º do Código do IVA:** Dedução fiscal e auto formal de quebras e destruição de mercadorias perecíveis sem liquidação de IVA compensatório.
  - **Artigo 23.º do Código do IRC:** Justificação e apuramento do CMVC real para efeitos fiscais.
  - Taxas de IVA legais em vigor: 6% (taxa reduzida), 13% (taxa intermédia) e 23% (taxa normal).
  - Encargos laborais com **TSU patronal de 23,75%** e 14 meses de remuneração.

---

## 🎨 Paleta de Cores Corporativa de Finanças e Tecnologia

- **Azul-Marinho Profundo (`#0F172A` / `#0b1120`):** Transmite robustez institucional, autoridade e rigor analítico.
- **Verde-Investimento (`#10B981` / `#059669`):** Destaca margem recuperada, ROI e ganhos líquidos de tesouraria.
- **Branco Puro (`#FFFFFF`) e Cinza Claro (`#F8FAFC` / `#F1F5F9`):** Fundo clean, moderno e de altíssima legibilidade executiva.
- **Acentos Funcionais:** Âmbar suave para atenção/ajuste e Coral/Rosa para alertas de roturas e quebras.

---

## 🚀 Como Iniciar o Servidor Django

### Opção 1: Arquivo Executável (.bat)
Dê um duplo clique no arquivo:
```
iniciar_servidor.bat
```

### Opção 2: Terminal / PowerShell
```bash
python manage.py runserver 127.0.0.1:8000
```

Abra o seu navegador em:
👉 **http://127.0.0.1:8000/**

Acesso ao Painel Administrativo do Django:
👉 **http://127.0.0.1:8000/admin/**
- **Utilizador:** `admin`
- **Palavra-passe:** `admin123`

---

## 🧭 Mapa da Aplicação (Rotas & Módulos)

| Rota | Descrição do Módulo |
|---|---|
| `/` | **SPA Principal:** Hero, Espelho Financeiro, Diagnóstico 360º, BI Embutido, Calculadora, Área de Contabilistas e Casos de Sucesso |
| `/dashboard/` | **Retail Intelligence 360º:** Ecrã dedicado com os 5 ecrãs de BI em ecrã completo |
| `/verificacao/` | **Áreas de Verificação:** Checklists operacionais de chão de loja (Cais, Talho, FLV e Caixas) |
| `/relatorios/` | **Central de Relatórios:** Listagem de relatórios de CMVC, SAF-T e Autos de Quebra |
| `/relatorios/<id>/` | **Dossiê Formal:** Folha timbrada oficial A4 pronta para impressão/PDF perante a AT e CC |
| `/documentos/` | **Minutas & Fichas:** Biblioteca normativa (Art.º 86.º CIVA, POPs de Cais e Ficha de Desmanche) |
| `/api/...` | Endpoints REST/AJAX assíncronos para simulação de margens e captação de leads |

---

## 💡 As 9 Funcionalidades Chave Implementadas

1. **Cabeçalho & Menu Superior Fixo:**
   - Logótipo da marca *Novo Varejo Inteligência de Mercado / Regis Costa*.
   - Navegação SPA suave e botão CTA *"Simular Recuperação de Margem"* com abertura de modal interativo.

2. **Hero Section de Alto Impacto:**
   - Headline: *"Proteja a Margem, Elimine Quebras e Recupere o Lucro Real do seu Supermercado em Portugal."*
   - Prova social em números animados (+72.000€/ano, 15 dias, 100% alinhado com o retalho português).
   - Ticker de insígnias atendidas: *Meu Super, Spar, Coviran, Amanhecer, Independentes*.

3. **Secção de Dor: "O Espelho Financeiro":**
   - Comparativo interativo: Ilusão do POS (24,5%) vs. Realidade do Chão de Loja (19,5%).
   - Tabela comparativa dinâmica com botões de faturação (80k€, 120k€, 200k€, 350k€/mês).

4. **Diagnóstico Raio-X 360º (15 Dias):**
   - Roteiro cirúrgico em 4 passos:
     * Dias 1 a 3: Processamento analítico (SAF-T, Curva ABC, CMVC e IVA).
     * Dias 4 a 7: Imersão presencial e auditoria de frescos (Talho, Charcutaria, Padaria, FLV).
     * Dias 8 a 10: Operação de cais, receção cega e produtividade laboral (TSU e horários).
     * Dias 11 a 15: Entrega do Relatório Executivo e plano de choque de 90 dias.
   - **Garantia Comercial:** 100% do valor do Raio-X abatido na primeira anuidade da avença.

5. **Painel de BI Interativo Embutido (Retail Intelligence 360º):**
   - **Aba 1 (Pulso de Tesouraria):** Margem de ecrã vs. real, árvore de fugas e simulador de ROI da avença com slider.
   - **Aba 2 (Blindagem de Preços):** 142 SKUs da Curva A com spread de custo do cais vs. PVP e simulação ao vivo.
   - **Aba 3 (Matriz ABC & Stock):** Análise das Curvas A, B e C, capital imobilizado e roturas fantasma com botão de auditar.
   - **Aba 4 (Raio-X dos Frescos):** Calculadora interativa de desmanche no talho (peso da carcaça, aparas, osso, custo real limpo e PVP mínimo) e controlo de quebra FLV.
   - **Aba 5 (Alertas Ativos):** Motor de notificações automáticas via WhatsApp para o sócio-gerente e chefe de loja.

6. **Secção Exclusiva para Contabilistas Certificados (CC):**
   - Parcerias B2B com gabinetes de contabilidade.
   - Saneamento do SAF-T, conferência de IVA e emissão de Autos de Abate (Art.º 86.º CIVA).
   - Modal com a *Tabela de Vantagens para Gabinetes de Contabilidade*.

7. **Calculadora de Potencial de Fugas e Ganhos:**
   - Sliders em tempo real: Faturação mensal (50.000€ a 400.000€), número de caixas e colaboradores.
   - Estimativa algorítmica imediata da fuga mensal/anual e botão para descarregar o relatório ou agendar a visita.

8. **Casos de Sucesso Reais e Depoimentos Auditados:**
   - *Supermercado da Vila Lda.* (Sintra • +64.000€ recuperados).
   - *Minimercado & Frescos do Minho* (Braga • +48.000€ recuperados).
   - *Alentejo Frescos & Mercearia* (Évora • +52.000€ recuperados).

9. **Rodapé Institucional PT-PT:**
   - Sede e delegações em Lisboa e Porto, NIPC português, conformidade RGPD e contactos diretos de apoio ao retalhista.
