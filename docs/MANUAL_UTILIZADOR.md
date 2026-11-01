# 📖 Manual do Utilizador: Tic-Tac-Toe AI

Bem-vindo ao **Tic-Tac-Toe AI**, o clássico Jogo do Galo reinventado com uma interface moderna e Inteligência Artificial!

---

## 1. Requisitos do Sistema
- **Sistema Operativo**: Windows 10/11, macOS ou Linux.
- **Python**: Versão 3.10 ou superior instalada.
- **Navegador Web**: Google Chrome, Mozilla Firefox, Microsoft Edge ou Safari.
- *(Opcional)* **Ollama**: Para utilizar modelos de linguagem locais (como `llama3.2`, `mistral` ou `phi3`). Se o Ollama não estiver instalado ou ativo, o jogo utiliza automaticamente o motor Minimax integrado.

---

## 2. Instalação e Execução

### Passo 1: Abrir o Terminal
Aceda à pasta do projeto no PowerShell ou Terminal:
```powershell
cd C:\Users\angel\nicegui_demo
```

### Passo 2: Instalar as Dependências
Instale as bibliotecas necessárias com um único comando:
```powershell
pip install -r requirements.txt
```

### Passo 3: Iniciar o Jogo
Execute a aplicação Python:
```powershell
python main.py
```

### Passo 4: Aceder à Interface
Abra o seu navegador de internet no seguinte endereço:
👉 **[http://localhost:8080](http://localhost:8080)**

---

## 3. Guia de Funcionalidades da Interface

A aplicação organiza-se em 4 abas principais no topo do ecrã:

### 🎮 1. Aba "Jogo"
- **Tabuleiro 3x3 Interativo**:
  - Clique em qualquer célula vazia para colocar o seu símbolo (`X`, azul).
  - A Inteligência Artificial responderá automaticamente com o símbolo (`O`, rosa/roxo).
- **Mente da IA (Diálogos Dinâmicos)**:
  - Abaixo ou ao lado do tabuleiro, a IA expressa os seus "pensamentos" e comentários provocatórios através de um balão de fala.
  - Um badge indica se a jogada foi gerada pelo modelo **Ollama** ou pelo algoritmo **Minimax**.
- **Placar em Tempo Real**:
  - Exibe instantaneamente as suas Vitórias, Derrotas e Empates acumulados.
- **Botão "Nova Partida"**:
  - Reinicia o tabuleiro a qualquer momento mantendo o histórico de pontuação.

---

### 📊 2. Aba "Estatísticas & Gráficos"
- **Gráfico Interativo de Pizza (ECharts)**:
  - Apresenta a percentagem e distribuição visual de vitórias suas vs. vitórias da IA vs. empates.
- **Tabela de Partidas Recentes**:
  - Registo detalhado das últimas partidas com data/hora, vencedor, número de jogadas e motor utilizado.
- **Botão "Atualizar Dados"**:
  - Atualiza as visualizações caso tenham sido jogadas novas partidas.

---

### 📜 3. Aba "Histórico & Ficheiros"
- Permite inspecionar em tempo real os ficheiros persistentes criados pelo sistema:
  - **`game_history.txt`**: Registo legível em texto corrido com data, jogadas e duração de cada partida.
  - **`matches.csv`**: Ficheiro de métricas estruturadas compatível com Excel e ferramentas de análise.

---

### ⚙️ 4. Aba "Configurações"
- **Nome do Jogador**: Personalize o seu nome que surgirá nas partidas e no histórico.
- **Personalidade da IA**:
  - *Sarcástico*: Provocações com humor negro.
  - *Amigável*: Comentários simpáticos e encorajadores.
  - *Científico*: Análise fria e probabilidades matemáticas.
- **Dificuldade Minimax**:
  - *Fácil*: Comete erros com frequência.
  - *Médio*: Jogador casual equilibrado.
  - *Imbatível*: Joga sempre de forma matematicamente ótima.
- **Parâmetros Ollama**:
  - Permite configurar o endereço (`http://localhost:11434`) e o nome do modelo (ex: `llama3.2`, `mistral`).
  - O botão **"Guardar e Testar Conexão"** verifica se o serviço Ollama está a responder.
- **Tema Escuro / Claro**:
  - Alterne entre o modo escuro e claro clicando no ícone no canto superior direito.

---

## 4. (Opcional) Como Ativar o Ollama no seu PC

Se quiser ver os comentários gerados em tempo real pelo modelo generativo:
1. Descarregue e instale o Ollama em [ollama.com](https://ollama.com).
2. No seu terminal, descarregue um modelo leve (exemplo):
   ```powershell
   ollama run llama3.2
   ```
3. Aceda à aba **⚙️ Configurações** na aplicação e clique em **"Guardar e Testar Conexão"**.
4. O badge no cabeçalho mudará para **"Ollama Online"**!

---

## 5. Resolução de Problemas (FAQ)

- **A aplicação diz "Ollama Offline", posso jogar na mesma?**
  - **Sim!** O sistema possui fallback automático. Se o Ollama não estiver a correr, o motor algorítmico Minimax assume o controlo das jogadas de forma transparente.
- **Onde ficam gravados os meus dados?**
  - Ficam guardados localmente na pasta `data/` do projeto (`data/logs`, `data/metrics`, `data/config` e `data/db`).
- **Como correr os testes de verificação?**
  - Execute: `python -m unittest discover -s tests` no terminal.
