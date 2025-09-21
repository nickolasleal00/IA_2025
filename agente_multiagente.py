from langchain_google_genai import ChatGoogleGenerativeAI
from  crewai import Agent, Task, Crew, Process, LLM

import os 

os.environ["GOOGLE_API"] = "AIzaSyDTDxpV3-k-UE1cOT1dvRTyI4EIdQDy9Tg"

llm = LLM(model='gemini/gemini-2.0-flash-lite', verbose=True, 
          temperature=0.4, api_key=os.environ["GOOGLE_API"])

print("Feito!")

analista_sintatico = Agent(
    role = "Parser de Logs de Servidor",
    goal = "Ler o conteúdo bruto de arquivos de log e convertê-lo em um formato estruturado (como CSV) usando código Python",
    backstory = "Profissional especialista em expressões regulares e na estruturação de dados não formatados.",
    verbose = True,
    llm = llm
)

analista_dados = Agent(
    role = "Analista de dados",
    goal = "Analisar os dados estruturados dos logs para encontrar padrões e erros",
    backstory = "Profissional que analisa dados proficientes em Python e na biblioteca Pandas",
    verbose = True,
    llm = llm
)

analista_relatorios = Agent(
    role = "Analista de relatórios",
    goal = "Compilar as análises de dados em um relatório final claro, conciso e fácil",
    backstory = "Profissional comunicador técnico que transforma dados brutos e análises em relatórios bem formatados em Markdown.",
    llm = llm
)

tarefa_criacao = Task (
    description ="Ler o arquivo de log 'access.log' usando a ferramenta de leitura de arquivo, criar e executar um script Python que extraia: Ip, data, método, URL e status.",
    expected_output = "Mensagem de confirmação de que o arquivo 'parsed_log.csv' foi criado com sucesso.",
    agent = analista_sintatico
)

tarefa_analisarDados = Task(
    description = "Usar a ferramenta de execução de código para criar e executar um script Python com a biblioteca pandas que carregue os dados do arquivo criado que identifique as 10 URLs mais acessadas," \
    "quantidade de erros, o IP que mais fez requisições e faça um print resumindo todas essas descobertas",
    expected_output = "Uma string de texto (print) contendo o resumo da análise: Top 10 URLs, contagem de erros e o IP mais frequente.",
    agent = analista_dados    
)

tarefa_gerarRelatorios = Task(
    description = "Com base no resumo da análise fornecido pela tarefa anterior, crie um relatório técnico completo em formato Markdown, contendo títulos:\n"
        "- Relatório de Análise de Logs do Servidor \n"
        "- Data da Análise: (coloque a data de hoje, 20 de setembro de 2025) \n"
        "- Resumo da Performance (incluindo as Top 10 URLs) \n"
        "- Análise de Erros \n"
        "- Análise de Segurança (incluindo o IP mais frequente e uma recomendação) \n",
    expected_output = "O relatório final completo em formato Markdown.",
    agent = analista_relatorios 
)

crew = Crew(
    agents = [analista_sintatico, analista_dados, analista_relatorios],
    tasks = [tarefa_criacao, tarefa_analisarDados, tarefa_gerarRelatorios],
    process = Process.sequential,
    verbose=True,
    llm = llm
)

resultado = crew.kickoff()
print(resultado)