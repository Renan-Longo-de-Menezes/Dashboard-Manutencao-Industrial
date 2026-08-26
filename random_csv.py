import numpy as np
import pandas as pd
import calendar

# ----------------------------------------------------------------------
# Configurações
# ----------------------------------------------------------------------
ANO = 2026
SEED = 42
np.random.seed(SEED)

# Proporções-base de Janeiro
TOTAL_JAN = 1000
CORRETIVAS_JAN = 648
PREVENTIVAS_JAN = 280
PREDITIVAS_JAN = 72

BASE_CORRETIVA = CORRETIVAS_JAN / TOTAL_JAN    # 0.648
BASE_PREVENTIVA = PREVENTIVAS_JAN / TOTAL_JAN  # 0.280
BASE_PREDITIVA = PREDITIVAS_JAN / TOTAL_JAN    # 0.072

# ----------------------------------------------------------------------
# Catálogos de dados para gerar descrições realistas
# ----------------------------------------------------------------------

# Equipamentos/Componentes
EQUIPAMENTOS = [
    "AGV", "CARRETA", "ESTEIRA", "EMPILHADEIRA", "TRANSPORTADOR",
    "PONTU ROLANTE", "ELETRÓLISE", "FORNO", "CALDEIRA", "COMPRESSOR",
    "BOMBA HIDRÁULICA", "MOTOR ELÉTRICO", "VENTILADOR INDUSTRIAL",
    "SISTEMA PNEUMÁTICO", "PAINEL ELÉTRICO", "SENSOR", "VÁLVULA",
    "REDUTOR", "CORREIA TRANSPORTADORA", "RODÍZIO", "TAPUME",
    "ALMOFADA", "ENGATE", "SAPATA", "CÂMBIO", "TAPACARIA",
    "SENSOR ÓPTICO", "MÓDULO DE CONTROLE", "BATERIA", "INVERSOR"
]

# Ações por tipo de manutenção
ACOES_PREVENTIVA = [
    "INSPEÇÃO", "LUBRIFICAÇÃO", "APERTO DE PARAFUSOS", "VERIFICAÇÃO",
    "SUBSTITUIÇÃO PROGRAMADA", "CALIBRAÇÃO", "LIMPEZA", "AJUSTE",
    "TESTE DE FUNCIONAMENTO", "TROCA DE ÓLEO", "VERIFICAÇÃO DE NÍVEL",
    "INSPEÇÃO VISUAL", "MEDIÇÃO DE VIBRAÇÃO", "TESTE DE ISOLAMENTO"
]

ACOES_CORRETIVA = [
    "TROCA", "REPARO", "SUBSTITUIÇÃO", "COLAGEM", "SOLDAGEM",
    "RETIFICAÇÃO", "REALINHAMENTO", "RECONSTRUÇÃO", "REMOÇÃO",
    "INSTALAÇÃO", "COLOCAÇÃO", "REVISÃO", "CORREÇÃO", "ELIMINAÇÃO"
]

ACOES_PREDITIVA = [
    "ANÁLISE", "MONITORAMENTO", "DIAGNÓSTICO", "INSPEÇÃO TERMOGRÁFICA",
    "ANÁLISE DE VIBRAÇÃO", "ULTRASSOM", "INSPEÇÃO POR CORRENTES FOUCAULT",
    "ANÁLISE DE ÓLEO", "TESTE NÃO DESTRUTIVO", "INSPEÇÃO ENDOSCÓPICA"
]

# Componentes específicos
COMPONENTES = [
    "PINTURA", "RODÍZIOS", "ENGATE", "ASSOALHO", "SAPATA",
    "CÂMBIO", "TAPEÇARIA", "ALMOFADA", "SENSORES", "ESTEIRA",
    "CORREIA", "MOTOR", "BOMBA", "VÁLVULA", "PAINEL", "FIAÇÃO",
    "ROLAMENTO", "EIXO", "EMBREAGEM", "FREIO", "SUSPENSÃO",
    "DIREÇÃO", "TRANSMISSÃO", "RADIADOR", "FILTRO", "TUBULAÇÃO"
]

# Locais/Áreas
LOCAIS = [
    "TIME 1", "TIME 2", "TIME 3", "TIME 4", "TIME 5", "TIME 6",
    "ÁREA LARANJA", "ÁREA AZUL", "ÁREA VERDE", "ÁREA VERMELHA",
    "SETOR A", "SETOR B", "SETOR C", "SETOR D",
    "LINHA 1", "LINHA 2", "LINHA 3",
    "GARAGEM", "OFICINA", "DEPÓSITO"
]

# Áreas específicas para descrições
AREAS_DESCRICAO = [
    "AREA LARANJA", "AREA AZUL", "AREA VERDE", "AREA VERMELHA",
    "SETOR A", "SETOR B", "SETOR C", "GARAGEM", "OFICINA PRINCIPAL",
    "LINHA DE PRODUÇÃO 1", "LINHA DE PRODUÇÃO 2", "DEPÓSITO CENTRAL"
]


def gerar_descricao(tipo_manutencao, equipamento, componente=None):
    """Gera uma descrição única e realista para a OS."""
    if tipo_manutencao == "Preventiva":
        acao = np.random.choice(ACOES_PREVENTIVA)
        if componente:
            return f"{acao} DE {componente} DO {equipamento}"
        else:
            area = np.random.choice(AREAS_DESCRICAO)
            return f"{acao} DA {area}"
    
    elif tipo_manutencao == "Corretiva":
        acao = np.random.choice(ACOES_CORRETIVA)
        if componente:
            return f"{acao} DE {componente} DO {equipamento}"
        else:
            componente = np.random.choice(COMPONENTES)
            return f"{acao} DE {componente} DO {equipamento}"
    
    else:  # Preditiva
        acao = np.random.choice(ACOES_PREDITIVA)
        if componente:
            return f"{acao} DE {componente} DO {equipamento}"
        else:
            componente = np.random.choice(COMPONENTES)
            return f"{acao} DE {componente} DO {equipamento}"


def gerar_linhas(mes, tipos, os_inicial):
    """Gera as linhas de um mês com descrições únicas."""
    linhas = []
    ndias = calendar.monthrange(ANO, mes)[1]
    os_numero = os_inicial

    for tipo in tipos:
        dia = np.random.randint(1, ndias + 1)
        data = f"{ANO}-{mes:02d}-{dia:02d}"
        
        equipamento = np.random.choice(EQUIPAMENTOS)
        componente = np.random.choice(COMPONENTES) if np.random.random() > 0.3 else None
        local = np.random.choice(LOCAIS)
        
        descricao = gerar_descricao(tipo, equipamento, componente)
        
        # Horas de parada e custo (correlacionados, por tipo)
        if tipo == "Corretiva":
            horas = round(np.random.uniform(3.0, 9.0), 1)
            custo = int(round(horas * np.random.uniform(400, 520), -1))
            p_atraso = 0.12
        elif tipo == "Preventiva":
            horas = round(np.random.uniform(1.0, 3.0), 1)
            custo = int(round(horas * np.random.uniform(180, 300), -1))
            p_atraso = 0.05
        else:  # Preditiva
            horas = round(np.random.uniform(0.5, 2.0), 1)
            custo = int(round(horas * np.random.uniform(500, 750), -1))
            p_atraso = 0.04
        
        status = "ATRASADA" if np.random.random() < p_atraso else "CONCLUÍDA"
        
        linhas.append([
            os_numero,
            descricao,
            local,
            status,
            tipo,
            data,
            custo
        ])
        
        os_numero += 1

    return linhas, os_numero


# ----------------------------------------------------------------------
# Geração mês a mês
# ----------------------------------------------------------------------
todas_linhas = []
resumo = []
os_atual = 5529729  # Começa do número que você mostrou

for mes in range(1, 13):
    if mes == 1:
        # Janeiro: valores exatos de referência
        total = TOTAL_JAN
        n_corretiva, n_preventiva, n_preditiva = 648, 280, 72
    else:
        # Demais meses: total e proporções próximos, com ruído aleatório
        total = int(np.random.randint(930, 1070))

        p_corr = BASE_CORRETIVA + np.random.uniform(-0.03, 0.03)
        p_prev = BASE_PREVENTIVA + np.random.uniform(-0.03, 0.03)
        p_pred = BASE_PREDITIVA + np.random.uniform(-0.02, 0.02)

        props = np.array([p_corr, p_prev, p_pred])
        props = np.clip(props, 0.02, None)
        props = props / props.sum()

        n_corretiva, n_preventiva, n_preditiva = np.random.multinomial(total, props)

    # Lista de tipos para este mês
    tipos = (["Corretiva"] * n_corretiva +
             ["Preventiva"] * n_preventiva +
             ["Preditiva"] * n_preditiva)
    np.random.shuffle(tipos)

    linhas_geradas, os_atual = gerar_linhas(mes, tipos, os_atual)
    todas_linhas.extend(linhas_geradas)
    resumo.append([f"{ANO}-{mes:02d}", total, n_corretiva, n_preventiva, n_preditiva])


# ----------------------------------------------------------------------
# Monta e salva o DataFrame
# ----------------------------------------------------------------------
df = pd.DataFrame(
    todas_linhas,
    columns=["OS", "DESCRIÇÃO_DA_TAREFA", "LOCAL", "STATUS", "TIPO_DE_MANUTENÇÃO", "DATA", "CUSTO"]
)
df["DATA"] = pd.to_datetime(df["DATA"])
df = df.sort_values("DATA").reset_index(drop=True)

df.to_csv("dados_manutencao.csv", index=False)

# ----------------------------------------------------------------------
# Verificação
# ----------------------------------------------------------------------
resumo_df = pd.DataFrame(
    resumo,
    columns=["Mês", "Total", "Corretiva", "Preventiva", "Preditiva"]
)
resumo_df["%Corretiva"] = (resumo_df["Corretiva"] / resumo_df["Total"] * 100).round(1)
resumo_df["%Preventiva"] = (resumo_df["Preventiva"] / resumo_df["Total"] * 100).round(1)
resumo_df["%Preditiva"] = (resumo_df["Preditiva"] / resumo_df["Total"] * 100).round(1)

print("Resumo mensal gerado:")
print(resumo_df.to_string(index=False))
print(f"\nTotal de ordens de serviço no ano: {len(df)}")
print("\nPrimeiras 10 linhas:")
print(df.head(10).to_string(index=False))
