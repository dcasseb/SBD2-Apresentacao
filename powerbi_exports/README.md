# 📊 Power BI - Artefatos Prontos para Importação

**Data de Geração:** 2026-02-02
**Projeto:** Crime Data Analytics - SBD2 Apresentação

---

## 📁 Arquivos Gerados

### 1. Queries SQL (5 arquivos)

Queries otimizadas para cada dashboard:

- `dashboard_1_overview.sql` - Visão geral com KPIs principais
- `dashboard_2_temporal.sql` - Análise temporal detalhada
- `dashboard_3_geographic.sql` - Dados geográficos para mapas
- `dashboard_4_victims_weapons.sql` - Perfil de vítimas e armas
- `dashboard_5_advanced.sql` - Análises avançadas com CTEs

### 2. Medidas DAX (`dax_measures.dax`)

Medidas prontas para copiar e colar no Power BI:
- Medidas básicas (Total Crimes, Violent Crime Rate)
- Medidas temporais (YoY Change, Moving Average)
- Medidas geográficas (Area Rank, Crime Density)
- Medidas avançadas (Risk Score, Hotspot Classification)

### 3. Estrutura de Dashboards (`dashboard_structure.json`)

Blueprint JSON com layout completo dos 3 dashboards principais:
- Tipos de visualizações
- Posicionamento (x, y, width, height)
- Medidas e dimensões a usar
- Configurações de formatação

---

## 🚀 Como Usar no Power BI

### Método 1: Importar Queries SQL Diretamente

1. **Abrir Power BI Desktop**

2. **Obter Dados → PostgreSQL database**
   - Servidor: `localhost`
   - Porta: `5432`
   - Database: `crime_data`
   - Usuário: `postgres`
   - Senha: `postgres`

3. **Clicar em "Advanced Options"**

4. **Copiar e colar uma das queries SQL** no campo "SQL statement"
   - Exemplo: Abrir `dashboard_1_overview.sql` e colar o conteúdo

5. **Clicar em OK → Load**

6. **Repetir para cada dashboard** (criar múltiplas queries)

---

### Método 2: Importar Tabelas e Usar Relacionamentos

1. **Conectar ao PostgreSQL** (mesmos passos acima)

2. **Selecionar as tabelas do schema `gold`:**
   - `gold.fato_crimes`
   - `gold.dim_area`
   - `gold.dim_crime_type`
   - `gold.dim_date`
   - `gold.dim_time`
   - `gold.dim_weapon`
   - `gold.dim_premise`
   - `gold.dim_victim`

3. **Clicar em "Transform Data"** para abrir Power Query Editor

4. **Verificar relacionamentos automáticos** em "Model View"
   - Power BI deve detectar automaticamente as FKs

5. **Fechar e Aplicar**

---

## 📐 Criar Medidas DAX

1. **Ir para "Model View"** ou "Data View"

2. **Clicar com botão direito** em qualquer tabela (ex: `fato_crimes`)

3. **Selecionar "New Measure"**

4. **Abrir o arquivo `dax_measures.dax`**

5. **Copiar e colar as medidas uma por uma**

Exemplo:
```dax
Total Crimes = COUNTROWS(fato_crimes)
```

6. **Pressionar Enter** para criar a medida

7. **Repetir** para todas as medidas desejadas

---

## 🎨 Criar Visualizações

### Dashboard 1: Visão Geral

**1. KPI Cards (4 cards no topo)**

- Inserir → Visualizações → Card
- Arrastar medida: `Total Crimes`
- Repetir para: `Violent Crime Rate`, `Most Dangerous Area`, `YoY Change %`

**2. Gráfico de Barras Horizontais**

- Inserir → Visualizações → Stacked Bar Chart
- Eixo Y: `dim_area[area_name]`
- Eixo X: `Total Crimes`
- Filtros: Top 10

**3. Gráfico de Pizza**

- Inserir → Visualizações → Pie Chart
- Legend: `dim_crime_type[crime_category]`
- Values: `Total Crimes`

**4. Gráfico de Linha**

- Inserir → Visualizações → Line Chart
- Eixo X: `dim_date[full_date]`
- Eixo Y: `Total Crimes`, `Violent Crimes`

---

### Dashboard 2: Análise Temporal

**1. Matrix Heatmap**

- Inserir → Visualizações → Matrix
- Rows: `dim_date[day_of_week]`
- Columns: `dim_time[hour]`
- Values: `Total Crimes`
- Formatar → Conditional Formatting → Background Color (escala de cores)

**2. Gráfico de Colunas**

- Inserir → Visualizações → Clustered Column Chart
- Eixo X: `dim_time[period_of_day]`
- Eixo Y: `Total Crimes`

**3. Gráfico de Área**

- Inserir → Visualizações → Area Chart
- Eixo X: `dim_date[month_name]`
- Eixo Y: `Total Crimes`, `Moving Average 3M`

---

### Dashboard 3: Análise Geográfica

**1. Mapa de Calor**

- Inserir → Visualizações → Map (ou Azure Maps se disponível)
- Location:
  - Latitude: `fato_crimes[latitude]`
  - Longitude: `fato_crimes[longitude]`
- Size: `Total Crimes`
- Legend: `dim_crime_type[crime_category]`

**2. Gráfico de Barras**

- Inserir → Visualizações → Stacked Bar Chart
- Eixo Y: `dim_area[area_name]`
- Eixo X: `Total Crimes`
- Legend: `Hotspot Classification`

---

## 🎯 Usando a Estrutura JSON

O arquivo `dashboard_structure.json` contém a "planta" completa dos dashboards.

**Como usar:**
1. Abrir o arquivo JSON
2. Ver a seção de cada dashboard
3. Para cada visual:
   - Verificar `type` (tipo de visualização)
   - Verificar `x_axis`, `y_axis` (campos a usar)
   - Verificar `position` (onde posicionar no canvas)
4. Replicar manualmente no Power BI Desktop

**Exemplo de um visual:**
```json
{
  "type": "bar_chart",
  "title": "Top 10 Áreas com Mais Crimes",
  "x_axis": "dim_area[area_name]",
  "y_axis": "Total Crimes",
  "sort": "descending",
  "top_n": 10,
  "position": {"x": 0, "y": 2, "width": 6, "height": 4}
}
```

Isso significa:
- Criar um gráfico de barras
- Eixo X: Nome da área
- Eixo Y: Total de crimes
- Ordenar decrescente
- Mostrar Top 10
- Posicionar no canvas nas coordenadas (0, 2)

---

## 🎨 Dicas de Formatação

### Paleta de Cores Recomendada

```
Violent Crime:    #D32F2F (Vermelho escuro)
Property Crime:   #F57C00 (Laranja)
Quality of Life:  #FBC02D (Amarelo)
Other Crime:      #1976D2 (Azul)

Gradiente de Intensidade:
Baixo:     #81C784 (Verde claro)
Médio:     #FFB74D (Laranja claro)
Alto:      #E57373 (Vermelho claro)
Crítico:   #D32F2F (Vermelho escuro)
```

### Aplicar Cores

1. Selecionar o visual
2. Format → Data colors → Custom colors
3. Inserir os códigos hex acima

---

## ✅ Checklist de Implementação

### Fase 1: Conexão
- [ ] Power BI Desktop instalado
- [ ] PostgreSQL rodando (Docker)
- [ ] Conexão testada e funcionando
- [ ] Queries SQL importadas ou tabelas carregadas

### Fase 2: Modelagem
- [ ] Relacionamentos verificados (auto-detect)
- [ ] Medidas DAX básicas criadas
- [ ] Medidas avançadas criadas
- [ ] Hierarquias temporais configuradas

### Fase 3: Visualizações
- [ ] Dashboard 1: Visão Geral
  - [ ] 4 KPI cards no topo
  - [ ] Gráfico de barras (Top 10 áreas)
  - [ ] Gráfico de pizza (categorias)
  - [ ] Gráfico de linha (tendência)
- [ ] Dashboard 2: Análise Temporal
  - [ ] Matrix heatmap (hora x dia)
  - [ ] Gráfico de colunas (período)
  - [ ] Gráfico de área (tendência)
- [ ] Dashboard 3: Análise Geográfica
  - [ ] Mapa de calor
  - [ ] Ranking de áreas
  - [ ] Tabela de detalhes

### Fase 4: Interatividade
- [ ] Slicers (filtros) adicionados
  - [ ] Filtro de data (ano/mês)
  - [ ] Filtro de região
  - [ ] Filtro de categoria de crime
- [ ] Cross-filtering configurado
- [ ] Drill-through configurado (se aplicável)
- [ ] Tooltips personalizados

### Fase 5: Finalização
- [ ] Títulos e descrições adicionados
- [ ] Cores aplicadas (paleta recomendada)
- [ ] Fontes e tamanhos ajustados
- [ ] Arquivo .pbix salvo
- [ ] Testado end-to-end

---

## 📊 Dados Disponíveis

### Estatísticas do Dataset

- **Total de Crimes:** 38,405 registros
- **Período:** 2020-2024
- **Áreas:** 21 áreas geográficas
- **Tipos de Crime:** 111 tipos únicos
- **Faixas Etárias:** 7 grupos etários
- **Dimensões:** 7 tabelas dimensionais
- **Tabela Fato:** 1 tabela (fato_crimes)

### Campos Principais

**Fato (fato_crimes):**
- sk_crime (PK)
- nk_crime_id
- latitude, longitude
- is_violent (boolean)
- created_at

**Dimensões:**
- dim_area: area_name, region
- dim_crime_type: crime_description, crime_category, is_violent
- dim_date: year, month, day, is_weekend
- dim_time: hour, period_of_day
- dim_victim: age_group, sex, descent
- dim_weapon: weapon_description, weapon_category
- dim_premise: premise_description

---

## 🔧 Troubleshooting

### Problema: Não consigo conectar ao PostgreSQL

**Solução:**
```bash
# Verificar se o container está rodando
docker ps --filter "name=sbd2_postgres"

# Se não estiver, iniciar
cd "SBD2-Apresentacao"
docker-compose up -d

# Verificar logs
docker logs sbd2_postgres
```

### Problema: Relacionamentos não foram detectados

**Solução:**
1. Ir para "Model View"
2. Clicar em "Manage Relationships"
3. Criar manualmente:
   - fato_crimes[sk_area] → dim_area[sk_area]
   - fato_crimes[sk_date] → dim_date[sk_date]
   - etc.

### Problema: Medidas DAX com erro

**Solução:**
- Verificar se os nomes das tabelas e colunas estão corretos
- Usar `fato_crimes[column]` em vez de `fato_crimes.column`
- Verificar se as medidas dependentes foram criadas primeiro

### Problema: Mapa não aparece

**Solução:**
- Verificar se os campos latitude/longitude estão preenchidos
- Alterar tipo de dados para "Decimal Number"
- Habilitar "Azure Maps" nas configurações do Power BI

---

## 📚 Recursos Adicionais

### Documentação Oficial
- Power BI Desktop: https://powerbi.microsoft.com/documentation/
- DAX Guide: https://dax.guide/
- PostgreSQL Connector: https://learn.microsoft.com/power-bi/connect-data/desktop-connect-postgresql

### Tutoriais
- Microsoft Learn - Power BI: https://learn.microsoft.com/training/powerplatform/power-bi
- Guy in a Cube (YouTube): https://www.youtube.com/c/GuyinaCube
- SQLBI: https://www.sqlbi.com/

---

## ✨ Próximos Passos

1. **Iniciar PostgreSQL**
   ```bash
   docker-compose up -d
   ```

2. **Abrir Power BI Desktop**
   - Conectar ao banco
   - Importar queries ou tabelas

3. **Criar Medidas DAX**
   - Copiar do arquivo `dax_measures.dax`

4. **Construir Dashboards**
   - Seguir estrutura do JSON
   - Adicionar visualizações uma a uma

5. **Testar e Validar**
   - Verificar números contra queries SQL
   - Testar filtros e interatividade

6. **Apresentar**
   - Salvar arquivo .pbix
   - Exportar para PDF/PowerPoint se necessário
   - Apresentar no PC2

---

**Tempo Estimado Total:** 3-4 horas

**Autor:** Claude Sonnet 4.5
**Projeto:** Crime Data Analytics - SBD2 Apresentação
