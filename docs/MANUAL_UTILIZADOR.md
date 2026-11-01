# Manual de Utilizador: Tic-Tac-Toe AI

Guia de instalação, configuração e utilização da aplicação Tic-Tac-Toe AI.

---

## 1. Requisitos de Sistema
- Sistema Operativo: Windows 10/11, macOS ou Linux.
- Python: Versão 3.10 ou superior.
- Navegador de Internet: Google Chrome, Microsoft Edge, Mozilla Firefox ou Safari.
- (Opcional) Ollama: Para inferência de linguagem natural através de modelos locais.

---

## 2. Instalação e Execução

### Passo 1: Aceder ao Diretório do Projeto
No terminal (PowerShell ou Bash):
```powershell
cd C:\Users\angel\nicegui_demo
```

### Passo 2: Instalar as Dependências
Execute o instalador de pacotes:
```powershell
pip install -r requirements.txt
```

### Passo 3: Executar a Aplicação
Inicie o servidor local:
```powershell
python main.py
```

### Passo 4: Abrir a Interface Web
Abra o navegador e aceda ao endereço:
http://localhost:8080

---

## 3. Descrição da Interface

A aplicação organiza-se em quatro secções acessíveis através do menu superior:

### 3.1 Jogo
- **Área de Tabuleiro**: Grelha 3x3 onde cada clique executa a jogada do jogador humano (símbolo X).
- **Resposta da IA**: A jogada do computador (símbolo O) é calculada e preenchida de forma automática.
- **Painel de Feedback**: Exibe o comentário produzido pelo modelo (ou algoritmo) e indica o motor utilizado no lance.
- **Placar**: Contador de vitórias, derrotas e empates obtidos na sessão.
- **Botão Nova Partida**: Limpa o tabuleiro e inicia um novo jogo sem reiniciar as estatísticas.

### 3.2 Estatísticas
- **Gráfico de Resultados**: Representação gráfica da distribuição de vitórias, derrotas e empates.
- **Tabela de Partidas Recentes**: Lista detalhada das partidas jogadas, incluindo data, vencedor, número de jogadas e tempo total.
- **Botão Atualizar**: Recarrega os registos mais recentes.

### 3.3 Histórico e Ficheiros
- Permite inspecionar diretamente os dados guardados em disco:
  - Ficheiro textual de log (`game_history.txt`).
  - Ficheiro tabular de métricas (`matches.csv`).

### 3.4 Configurações
- **Nome do Jogador**: Permite alterar o identificador associado às estatísticas.
- **Estilo de Resposta da IA**: Seleção entre os perfis Sarcástico, Amigável e Analítico.
- **Nível do Motor Minimax**: Ajuste da dificuldade heurística (Fácil, Médio, Imbatível).
- **Endereço e Modelo Ollama**: Configuração do endpoint HTTP e nome do modelo local.
- **Testar Conexão**: Verifica a disponibilidade do serviço Ollama na rede local.

---

## 4. Configuração Opcional do Ollama

Caso pretenda utilizar modelos de linguagem locais para os comentários e jogadas:
1. Instale o Ollama a partir do site oficial (https://ollama.com).
2. Transfira o modelo pretendido no seu terminal:
   ```powershell
   ollama pull llama3.2
   ```
3. Na aba Configurações da aplicação, certifique-se de que o campo do modelo coincide com o modelo descarregado e clique em "Guardar e Testar Conexão".
4. Caso o Ollama não esteja em execução, a aplicação continua totalmente funcional através do motor algorítmico Minimax.

---

## 5. Execução de Testes Automatizados

Para validar o funcionamento de todos os módulos e regras do sistema:
```powershell
python -m unittest discover -s tests
```
