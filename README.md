# Análise Exploratória de Dados: TV Shows

Higienização, padronização e análise exploratória de um conjunto de dados com programas de TV disponíveis em plataformas de streaming (Netflix, Hulu, Prime Video e Disney+), desenvolvido para a aula prática de **Análise Exploratória de Dados**, Unidade 2: Limpeza, Estruturação e Enriquecimento de Dados.

## Estrutura do projeto

```
.
├── app.py                                # Script principal da análise
├── requirements.txt                      # Dependências do projeto
├── tv_shows.csv                          # Dataset original (entrada)
├── tv_shows_tratado.csv                  # Dataset tratado, gerado após a higienização (saída)
├── gráfico/
│   └── top15_rotten_tomatoes.png         # Gráfico gerado pela análise
└── higienizacao_dados_cienc_dados.docx   # Relatório final da atividade
```

## Pré-requisitos

- Python 3.9 ou superior
- Bibliotecas listadas em `requirements.txt` (pandas e matplotlib)

## Instalação

Clone ou baixe o projeto e, na pasta raiz, crie e ative um ambiente virtual (venv) antes de instalar as dependências, pois isso evita conflitos com outros projetos Python instalados na máquina:

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

Com o ambiente virtual ativado (o terminal deve exibir `(venv)` no início da linha), instale as dependências:

```bash
pip install -r requirements.txt
```

## Como executar

Certifique-se de que o arquivo `tv_shows.csv` está na mesma pasta do `app.py` e execute:

```bash
python app.py
```

Ao final da execução:

- após o tratamento (higienização e padronização) dos dados, é gerada a planilha `tv_shows_tratado.csv`, com o dataset limpo;
- o gráfico com o Top 15 programas por nota do Rotten Tomatoes é salvo em `gráfico/top15_rotten_tomatoes.png`;
- os resultados da análise (linhas excluídas, médias de plataformas, rankings) são impressos no console.

## O que o script faz

1. **Carregamento**: lê o `tv_shows.csv` com pandas.
2. **Exploração inicial**: estrutura dos dados, resumo estatístico e contagem de valores nulos por coluna.
3. **Identificação de problemas e higienização**: remove colunas irrelevantes (`Unnamed: 0` e `Type`), verifica duplicatas por Título + Ano e remove linhas com valores nulos em `Age` e/ou `IMDb`.
4. **Padronização**: converte `IMDb` e `Rotten Tomatoes` de texto para número e traduz a classificação indicativa americana (`Age`) para a classificação indicativa brasileira.
5. **Organização**: ordena os programas de forma decrescente pela nota do Rotten Tomatoes, incluindo um ranking dentro de cada uma das 4 plataformas (Netflix, Hulu, Prime Video e Disney+).
6. **Visualização**: gera e salva o gráfico com os 15 programas mais bem avaliados.
7. **Análise dos resultados**: responde às perguntas de avaliação do roteiro (linhas excluídas, relação entre nota e número de plataformas, ranking geral).

## Relatório

O documento `higienizacao_dados_cienc_dados.docx` reúne o processo completo em formato de relatório: introdução, exploração, higienização, padronização, organização por plataforma, visualização, análise dos resultados e conclusão.

## Dataset

O arquivo `tv_shows.csv` reúne programas de TV disponíveis em quatro plataformas de streaming (Netflix, Hulu, Prime Video e Disney+), com título, ano, classificação indicativa, nota no IMDb e nota no Rotten Tomatoes.