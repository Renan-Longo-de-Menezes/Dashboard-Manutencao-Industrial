import re
from collections import Counter
from io import BytesIO

import pandas as pd 
import plotly.express as px 
import streamlit as st 

# ----------------------------------------------------------------------
# Configuração da página
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Dashboard de Manutenção",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

DIAS_SEMANA = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

# Palavras irrelevantes para a contagem de termos nas descrições
STOPWORDS = {
    "DE", "DO", "DA", "DOS", "DAS", "A", "O", "E", "EM", "PARA", "POR",
    "COM", "NA", "NO", "UM", "UMA", "AO", "OS", "AS", "QUE", "SE",
}


def formatar_moeda(valor):
    """Formata número no padrão brasileiro: 1234.5 -> R$ 1.234,50"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def extrair_acao(descricao):
    """Primeira palavra = ação da manutenção (ex: COLAGEM, REVISÃO)."""
    if not isinstance(descricao, str):
        return ""
    return descricao.split()[0]


def extrair_objeto(descricao):
    """Texto após o último 'DO'/'DA' = equipamento ou área alvo."""
    if not isinstance(descricao, str):
        return ""
    ocorrencias = re.findall(r"\b(?:DO|DA)\s+(.+)$", descricao, flags=re.IGNORECASE)
    return ocorrencias[-1].strip() if ocorrencias else ""


# ----------------------------------------------------------------------
# Dados de exemplo (mesma estrutura do CSV, com range de datas realista)
# ----------------------------------------------------------------------
@st.cache_data
def gerar_dados_exemplo():
    """Gera dados de exemplo com range de datas realista (jan a mar/2026)."""
    datas_exemplo = pd.date_range("2026-01-01", "2026-03-31", freq="D")

    descricoes = [
        "COLAGEM DE FREIO DO AGV",
        "REVISÃO DE CÂMBIO DO MÓDULO DE CONTROLE",
        "MEDIÇÃO DE VIBRAÇÃO DA AREA AZUL",
        "SUBSTITUIÇÃO DE FIAÇÃO DO CÂMBIO",
        "COLOCAÇÃO DE ESTEIRA DO BATERIA",
        "ELIMINAÇÃO DE SUSPENSÃO DO AGV",
        "TROCA DE RODÍZIOS DA CARRETA",
        "INSPEÇÃO DE PINTURA DO FORNO",
        "RETIFICAÇÃO DE MOTOR ELÉTRICO",
    ]
    locais = [
        "TIME 1", "TIME 2", "TIME 3", "TIME 4", "ÁREA VERMELHA",
        "ÁREA AZUL", "SETOR A", "SETOR B", "LINHA 1",
    ]
    status = [
        "CONCLUÍDA", "CONCLUÍDA", "CONCLUÍDA", "CONCLUÍDA", "ATRASADA",
        "CONCLUÍDA", "CONCLUÍDA", "CONCLUÍDA", "CONCLUÍDA",
    ]
    tipos = [
        "Corretiva", "Corretiva", "Preventiva", "Corretiva", "Corretiva",
        "Corretiva", "Preventiva", "Preditiva", "Corretiva",
    ]
    custos = [1850, 1540, 460, 2550, 2280, 3280, 1200, 800, 2100]

    total_linhas = len(datas_exemplo) * 3

    dados = {
        "OS": list(range(5530001, 5530001 + total_linhas)),
        "DESCRIÇÃO_DA_TAREFA": (descricoes * (total_linhas // len(descricoes) + 1))[:total_linhas],
        "LOCAL": (locais * (total_linhas // len(locais) + 1))[:total_linhas],
        "STATUS": (status * (total_linhas // len(status) + 1))[:total_linhas],
        "TIPO_DE_MANUTENÇÃO": (tipos * (total_linhas // len(tipos) + 1))[:total_linhas],
        "DATA": list(datas_exemplo) * 3,
        "CUSTO": (custos * (total_linhas // len(custos) + 1))[:total_linhas],
    }

    df = pd.DataFrame(dados)
    df["DATA"] = pd.to_datetime(df["DATA"])
    return df


def converter_excel(df):
    """Gera os bytes de um arquivo .xlsx a partir do DataFrame."""
    arquivo = BytesIO()
    with pd.ExcelWriter(arquivo, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Dados")
    return arquivo.getvalue()


# ----------------------------------------------------------------------
# Título
# ----------------------------------------------------------------------
st.title("🔧 Dashboard de Indicadores de Manutenção")
st.caption("Projeto de BI para acompanhamento de ordens de serviço e produtividade.")

# ----------------------------------------------------------------------
# Carregamento dos dados
# ----------------------------------------------------------------------
st.sidebar.header("📁 Fonte dos dados")
arquivo_csv = st.sidebar.file_uploader("Envie um arquivo CSV (opcional)", type=["csv"])

COLUNAS_ESPERADAS = {
    "OS", "DESCRIÇÃO_DA_TAREFA", "LOCAL", "STATUS",
    "TIPO_DE_MANUTENÇÃO", "DATA", "CUSTO",
}

if arquivo_csv is not None:
    try:
        df = pd.read_csv(arquivo_csv, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(arquivo_csv, encoding="latin-1")

    if not COLUNAS_ESPERADAS.issubset(df.columns):
        st.error(f"Colunas esperadas: {sorted(COLUNAS_ESPERADAS)}")
        st.error(f"Colunas encontradas: {list(df.columns)}")
        st.stop()

    df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce")
    st.sidebar.success(f"CSV carregado! {len(df):,} ordens de serviço.")
else:
    df = gerar_dados_exemplo()
    st.info("Você está visualizando dados de exemplo. Envie o CSV real na barra lateral.")

# ----------------------------------------------------------------------
# Filtros
# ----------------------------------------------------------------------
st.sidebar.header("🔎 Filtros")

# Período
min_data, max_data = df["DATA"].min().date(), df["DATA"].max().date()
intervalo = st.sidebar.date_input(
    "Período",
    value=(min_data, max_data),
    min_value=min_data,
    max_value=max_data,
)

tipos_selecionados = st.sidebar.multiselect(
    "Tipo de manutenção",
    options=sorted(df["TIPO_DE_MANUTENÇÃO"].dropna().unique()),
    default=sorted(df["TIPO_DE_MANUTENÇÃO"].dropna().unique()),
)

status_selecionados = st.sidebar.multiselect(
    "Status",
    options=sorted(df["STATUS"].dropna().unique()),
    default=sorted(df["STATUS"].dropna().unique()),
)

locais_selecionados = st.sidebar.multiselect(
    "Local / Time",
    options=sorted(df["LOCAL"].dropna().unique()),
    default=sorted(df["LOCAL"].dropna().unique()),
)

custo_min_df = int(df["CUSTO"].min())
custo_max_df = int(df["CUSTO"].max())
faixa_custo = st.sidebar.slider(
    "Faixa de custo (R$)",
    custo_min_df,
    custo_max_df,
    (custo_min_df, custo_max_df),
    step=50,
)

# Aplicação dos filtros
df_filtrado = df.copy()

if isinstance(intervalo, (tuple, list)) and len(intervalo) == 2:
    df_filtrado = df_filtrado[
        (df_filtrado["DATA"].dt.date >= intervalo[0])
        & (df_filtrado["DATA"].dt.date <= intervalo[1])
    ]

df_filtrado = df_filtrado[
    (df_filtrado["TIPO_DE_MANUTENÇÃO"].isin(tipos_selecionados))
    & (df_filtrado["STATUS"].isin(status_selecionados))
    & (df_filtrado["LOCAL"].isin(locais_selecionados))
    & (df_filtrado["CUSTO"].between(faixa_custo[0], faixa_custo[1]))
].copy()

# Colunas derivadas (para análises temporais e de texto)
df_filtrado["MES"] = df_filtrado["DATA"].dt.strftime("%m/%Y")
df_filtrado["DIA_SEMANA"] = df_filtrado["DATA"].dt.dayofweek.map(lambda d: DIAS_SEMANA[d])
df_filtrado["ACAO"] = df_filtrado["DESCRIÇÃO_DA_TAREFA"].map(extrair_acao)
df_filtrado["OBJETO"] = df_filtrado["DESCRIÇÃO_DA_TAREFA"].map(extrair_objeto)

# ----------------------------------------------------------------------
# KPIs
# ----------------------------------------------------------------------
total_os = len(df_filtrado)
custo_total = df_filtrado["CUSTO"].sum()
ticket_medio = custo_total / total_os if total_os > 0 else 0
concluidas = (df_filtrado["STATUS"] == "CONCLUÍDA").sum()
atrasadas = (df_filtrado["STATUS"] == "ATRASADA").sum()
pct_concluidas = (concluidas / total_os * 100) if total_os > 0 else 0
taxa_atraso = (atrasadas / total_os * 100) if total_os > 0 else 0
custo_atrasadas = df_filtrado.loc[df_filtrado["STATUS"] == "ATRASADA", "CUSTO"].sum()
num_locais = df_filtrado["LOCAL"].nunique()

st.subheader("📊 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Ordens de serviço", f"{total_os:,}")
col2.metric("Custo total", formatar_moeda(custo_total))
col3.metric("Ticket médio", formatar_moeda(ticket_medio))
col4.metric("OS concluídas", f"{pct_concluidas:.1f}%")

col5, col6, col7, col8 = st.columns(4)
col5.metric("OS atrasadas", f"{atrasadas:,}", f"{taxa_atraso:.1f}% do total")
col6.metric("Custo das atrasadas", formatar_moeda(custo_atrasadas))
col7.metric("Locais / Times", num_locais)
col8.metric("Custo médio (atrasadas)",
            formatar_moeda(custo_atrasadas / atrasadas) if atrasadas > 0 else "—")

st.divider()

if df_filtrado.empty:
    st.warning("Nenhuma ordem de serviço corresponde aos filtros selecionados.")
    st.stop()

# ----------------------------------------------------------------------
# Abas de análise
# ----------------------------------------------------------------------
aba_geral, aba_tempo, aba_texto, aba_tabela = st.tabs(
    ["📈 Visão Geral", "🕒 Tendências", "📝 Descrições", "🔍 Detalhamento"]
)

# ==================== ABA 1: VISÃO GERAL ====================
with aba_geral:
    c1, c2 = st.columns(2)

    with c1:
        os_por_tipo = (
            df_filtrado.groupby("TIPO_DE_MANUTENÇÃO", as_index=False)["OS"].count()
            .rename(columns={"OS": "Quantidade"})
        )
        fig_tipo = px.bar(
            os_por_tipo,
            x="TIPO_DE_MANUTENÇÃO",
            y="Quantidade",
            color="TIPO_DE_MANUTENÇÃO",
            title="Ordens de Serviço por Tipo de Manutenção",
            text_auto=True,
        )
        st.plotly_chart(fig_tipo, use_container_width=True)

    with c2:
        custo_por_tipo = (
            df_filtrado.groupby("TIPO_DE_MANUTENÇÃO", as_index=False)["CUSTO"].sum()
            .sort_values("CUSTO", ascending=False)
        )
        fig_custo_tipo = px.bar(
            custo_por_tipo,
            x="TIPO_DE_MANUTENÇÃO",
            y="CUSTO",
            color="CUSTO",
            title="Custo por Tipo de Manutenção",
            text_auto=".2s",
            color_continuous_scale="Reds",
        )
        st.plotly_chart(fig_custo_tipo, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        status_contagem = (
            df_filtrado.groupby("STATUS", as_index=False)["OS"].count()
            .rename(columns={"OS": "Quantidade"})
        )
        fig_status = px.pie(
            status_contagem,
            names="STATUS",
            values="Quantidade",
            title="Distribuição por Status",
            hole=0.45,
            color_discrete_sequence=["#2ecc71", "#e74c3c"],
        )
        fig_status.update_traces(textinfo="percent+value")
        st.plotly_chart(fig_status, use_container_width=True)

    with c4:
        top_locais = (
            df_filtrado.groupby("LOCAL", as_index=False)["OS"].count()
            .rename(columns={"OS": "Quantidade"})
            .sort_values("Quantidade", ascending=False)
            .head(15)
        )
        fig_local = px.bar(
            top_locais,
            x="Quantidade",
            y="LOCAL",
            orientation="h",
            title="Top 15 Locais por Nº de OS",
            text_auto=True,
            color="Quantidade",
            color_continuous_scale="Viridis",
        )
        fig_local.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_local, use_container_width=True)

# ==================== ABA 2: TENDÊNCIAS ====================
with aba_tempo:
    c1, c2 = st.columns(2)

    with c1:
        os_mes = (
            df_filtrado.groupby("MES", as_index=False)["OS"].count()
            .rename(columns={"OS": "Quantidade"})
        )
        fig_os_mes = px.line(
            os_mes, x="MES", y="Quantidade", markers=True,
            title="Evolução Mensal das Ordens de Serviço",
        )
        st.plotly_chart(fig_os_mes, use_container_width=True)

    with c2:
        custo_mes = df_filtrado.groupby("MES", as_index=False)["CUSTO"].sum()
        fig_custo_mes = px.area(
            custo_mes, x="MES", y="CUSTO",
            title="Custo Mensal",
        )
        st.plotly_chart(fig_custo_mes, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        os_dia_semana = (
            df_filtrado.groupby("DIA_SEMANA", as_index=False)["OS"].count()
            .rename(columns={"OS": "Quantidade"})
        )
        ordem_dias = [d for d in DIAS_SEMANA if d in os_dia_semana["DIA_SEMANA"].tolist()]
        fig_dia = px.bar(
            os_dia_semana,
            x="DIA_SEMANA", y="Quantidade",
            category_orders={"DIA_SEMANA": ordem_dias},
            title="Ordens de Serviço por Dia da Semana",
            text_auto=True,
        )
        st.plotly_chart(fig_dia, use_container_width=True)

    with c4:
        heatmap = (
            df_filtrado.groupby(["DIA_SEMANA", "MES"], as_index=False)["OS"].count()
            .rename(columns={"OS": "Quantidade"})
        )
        fig_heat = px.density_heatmap(
            heatmap, x="MES", y="DIA_SEMANA", z="Quantidade",
            title="Heatmap: OS por Dia da Semana × Mês",
            color_continuous_scale="Blues",
        )
        fig_heat.update_yaxes(categoryorder="array", categoryarray=DIAS_SEMANA)
        st.plotly_chart(fig_heat, use_container_width=True)

# ==================== ABA 3: DESCRIÇÕES ====================
with aba_texto:
    c1, c2 = st.columns(2)

    with c1:
        top_acoes = (
            df_filtrado.groupby("ACAO", as_index=False)["OS"].count()
            .rename(columns={"OS": "Quantidade"})
            .sort_values("Quantidade", ascending=False)
            .head(15)
        )
        fig_acao = px.bar(
            top_acoes, x="Quantidade", y="ACAO", orientation="h",
            title="Top 15 Ações mais Frequentes",
            text_auto=True, color="Quantidade",
            color_continuous_scale="Teal",
        )
        fig_acao.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_acao, use_container_width=True)

    with c2:
        top_objetos = (
            df_filtrado[df_filtrado["OBJETO"] != ""]
            .groupby("OBJETO", as_index=False)["OS"].count()
            .rename(columns={"OS": "Quantidade"})
            .sort_values("Quantidade", ascending=False)
            .head(15)
        )
        fig_objeto = px.bar(
            top_objetos, x="Quantidade", y="OBJETO", orientation="h",
            title="Top 15 Equipamentos / Áreas (extraído das descrições)",
            text_auto=True, color="Quantidade",
            color_continuous_scale="Plasma",
        )
        fig_objeto.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_objeto, use_container_width=True)

    # Palavras mais frequentes
    todas_palavras = []
    for desc in df_filtrado["DESCRIÇÃO_DA_TAREFA"].dropna():
        todas_palavras.extend(
            p for p in re.findall(r"[A-ZÀ-Ú0-9]+", desc.upper())
            if p not in STOPWORDS and len(p) > 2
        )
    contagem = Counter(todas_palavras).most_common(20)
    df_palavras = pd.DataFrame(contagem, columns=["Palavra", "Frequência"])

    st.markdown("#### ☁️ Palavras mais frequentes nas descrições")
    st.bar_chart(df_palavras.set_index("Palavra"))

# ==================== ABA 4: DETALHAMENTO ====================
with aba_tabela:
    busca = st.text_input(
        "Buscar por palavra-chave na descrição, OS ou local",
        placeholder="Ex: AGV, TROCA, TIME 1, 5530556...",
    )

    df_detalhe = df_filtrado.sort_values("DATA", ascending=False)

    if busca:
        mascara = (
            df_detalhe["DESCRIÇÃO_DA_TAREFA"].astype(str).str.contains(busca, case=False, na=False)
            | df_detalhe["OS"].astype(str).str.contains(busca, case=False, na=False)
            | df_detalhe["LOCAL"].astype(str).str.contains(busca, case=False, na=False)
            | df_detalhe["TIPO_DE_MANUTENÇÃO"].astype(str).str.contains(busca, case=False, na=False)
        )
        df_detalhe = df_detalhe[mascara]

    st.markdown(f"**{len(df_detalhe):,}** ordens de serviço encontradas.")
    st.dataframe(df_detalhe, use_container_width=True, hide_index=True)

    st.download_button(
        label="⬇️ Baixar dados filtrados (CSV)",
        data=df_detalhe.to_csv(index=False).encode("utf-8"),
        file_name="dados_manutencao_filtrados.csv",
        mime="text/csv",
    )
    st.download_button(
        label="⬇️ Baixar dados filtrados (Excel)",
        data=converter_excel(df_detalhe),
        file_name="dados_manutencao_filtrados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

# ----------------------------------------------------------------------
# Insights automáticos
# ----------------------------------------------------------------------
st.divider()
st.subheader("💡 Insights Automáticos")

with st.expander("Ver insights gerados a partir dos dados filtrados", expanded=True):
    tipo_dominante = os_por_tipo.loc[os_por_tipo["Quantidade"].idxmax()]

    insights = []
    insights.append(
        f"• O tipo **{tipo_dominante['TIPO_DE_MANUTENÇÃO']}** domina o período com "
        f"**{tipo_dominante['Quantidade']:,}** OS "
        f"({tipo_dominante['Quantidade'] / total_os * 100:.1f}% do total)."
    )
    insights.append(
        f"• A taxa de atraso é de **{taxa_atraso:.1f}%** "
        f"({atrasadas:,} OS), representando **{formatar_moeda(custo_atrasadas)}** em custo."
    )

    if not top_objetos.empty:
        obj_top = top_objetos.iloc[0]
        insights.append(
            f"• O equipamento/área mais citado é **{obj_top['OBJETO']}** "
            f"({obj_top['Quantidade']:,} ocorrências)."
        )

    if not top_locais.empty:
        local_top = top_locais.iloc[0]
        insights.append(
            f"• O local com mais OS é **{local_top['LOCAL']}** "
            f"({local_top['Quantidade']:,} OS)."
        )

    if len(os_mes) > 1:
        pico_mes = os_mes.loc[os_mes["Quantidade"].idxmax()]
        insights.append(
            f"• O mês com maior volume foi **{pico_mes['MES']}** "
            f"({pico_mes['Quantidade']:,} OS)."
        )

    for i in insights:
        st.markdown(i)
