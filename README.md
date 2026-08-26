# 🔧 Dashboard de Indicadores de Manutenção

Dashboard interativo desenvolvido em **Streamlit** para análise de ordens de serviço de manutenção industrial, com foco em indicadores de produtividade, custos e acompanhamento de equipes.

> Projeto inspirado na rotina real de uma planta industrial, utilizando dados simulados com base em cenários reais de manutenção Insdustrial e de equipamentos.

---

## 🎯 Objetivo

Facilitar a tomada de decisão de gestores e coordenadores de manutenção por meio de:

- Visualização clara de KPIs (custo total, ticket médio, taxa de atraso, etc.)
- Análise de tendências temporais (mensal e por dia da semana)
- Identificação de equipamentos, ações e locais mais críticos
- Detalhamento e exportação dos dados filtrados

---

## ✨ Funcionalidades

### 📊 Visão Geral
- OS por tipo de manutenção (Corretiva, Preventiva, Preditiva)
- Custo por tipo de manutenção
- Distribuição por status (Concluída / Atrasada)
- Top 15 locais com mais ordens de serviço

### 🕒 Tendências
- Evolução mensal das OS
- Custo mensal acumulado
- OS por dia da semana
- Heatmap de OS (dia da semana × mês)

### 📝 Análise de Descrições
- Top 15 ações mais frequentes
- Top 15 equipamentos/áreas mais citados
- Palavras mais recorrentes nas descrições

### 🔍 Detalhamento
- Busca por palavra-chave (OS, descrição, local, tipo)
- Tabela interativa com todos os dados filtrados
- Exportação em **CSV** e **Excel**

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|------------|-----|
| **Python 3.10+** | Linguagem base |
| **Streamlit** | Interface web interativa |
| **Pandas** | Manipulação e análise de dados |
| **Plotly** | Gráficos interativos |
| **OpenPyXL** | Exportação para Excel |
| **NumPy** | Geração de dados simulados |

---

## 🚀 Como Executar

### 1. Clone o repositório

	```bash
	git clone https://github.com/Renan-Longo-de-Menezes/Dashboard-Manutenção-Industrial.git
	cd dashboard-manutencao

### 2. Crie um ambiente virtual (recomendado)
	python -m venv venv

	# Windows
	venv\Scripts\activate

	# Linux/Mac
	source venv/bin/activate

### 3. Instale as dependências
	pip install -r requirements.txt

### 4. Execute o dashboard
	streamlit run app.py
	O dashboard será aberto automaticamente no navegador em http://localhost:8501.

---

📦 Gerando Novos Dados (caso não tenha arquivo CSV)
	O arquivo random_csv.py gera um ano completo de ordens de serviço simuladas (~12.000 OS), com distribuição realista entre manutenções corretivas, preventivas e preditivas.	
		python random_csv.py
	O arquivo dados_manutencao.csv será gerado/atualizado na raiz do projeto.

📂 Estrutura do Projeto
	.
	├── app.py                 # Dashboard Streamlit principal
	├── random_csv.py          # Script para gerar dados simulados
	├── dados_manutencao.csv   # Base de dados de exemplo
	├── requirements.txt       # Dependências do projeto
	└── README.md              # Este arquivo

🎨 Capturas de Tela
	<img width="2128" height="431" alt="image" src="https://github.com/user-attachments/assets/88bdfb83-da9e-4029-b163-946b63b8276e" />
	<img width="2196" height="960" alt="image" src="https://github.com/user-attachments/assets/ae13c826-a975-4115-b66a-68a8c83673c4" />
	<img width="2128" height="898" alt="image" src="https://github.com/user-attachments/assets/a23dd191-f50d-4d47-9bc8-de73f61ee373" />
	<img width="2128" height="845" alt="image" src="https://github.com/user-attachments/assets/c88cf7cc-eb7a-4005-9024-72dd50d954c5" />
	<img width="559" height="961" alt="image" src="https://github.com/user-attachments/assets/469f4024-f8f4-4f22-8bcb-4f1c5cbf20a3" />



---


💡 Próximos Passos (Roadmap)
 	Deploy na Streamlit Community Cloud
 	Adicionar análise de Pareto (80/20) por equipamento
 	Gráfico de custo acumulado por tipo de manutenção
 	Indicador de MTBF e MTTR
 	Integração com banco de dados real (PostgreSQL/MySQL)
 	Autenticação de usuários por perfil (gestor, técnico, etc.)


---

👨‍💻 Autor
Renan Longo de Menezes

📧 renan.lm@outlook.com
💼 https://www.linkedin.com/in/renan-longo-de-menezes
🐙 https://github.com/Renan-Longo-de-Menezes
