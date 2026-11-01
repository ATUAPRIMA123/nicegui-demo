# 🎮 Tic-Tac-Toe AI (Jogo do Galo com IA)

Uma aplicação interativa de Jogo do Galo desenvolvida em **Python** e **NiceGUI**, com motor híbrido de Inteligência Artificial (**Ollama LLM** + **Minimax**) e persistência poliglota (**TXT, CSV, JSON e SQLite**).

---

## 🚀 Como Executar

1. **Instalar dependências**:
   ```powershell
   pip install -r requirements.txt
   ```

2. **Iniciar o jogo**:
   ```powershell
   python main.py
   ```

3. **Abrir no browser**:
   Aceda a [http://localhost:8080](http://localhost:8080).

4. **Correr a suite de testes automatizados**:
   ```powershell
   python -m unittest discover -s tests
   ```

---

## 📋 Requisitos Técnicos Cumpridos

- ✅ **Implementação em Python** (3.10+)
- ✅ **Programação Modular**:
  - `core/board.py`: Lógica do tabuleiro, validações e regras de jogo.
  - `core/exceptions.py`: Hierarquia de exceções personalizadas (`InvalidMoveError`, `PositionOccupiedError`, etc.).
  - `ai/ollama_engine.py`: Integração com API Ollama e tratamento de fallback.
  - `ai/minimax.py`: Algoritmo Minimax com níveis de dificuldade.
  - `storage/persistence.py`: Gestão de persistência multi-formato.
  - `main.py`: Interface gráfica reativa.
- ✅ **Estruturas de Dados Adequadas**: Matrizes 3x3, tuplos de coordenadas, dicionários de estado, dataclasses e listas dinâmicas.
- ✅ **Validação de Dados e Tratamento de Exceções**: Verificação de limites, casas ocupadas, sanitização de inputs e tolerância a falhas na API.
- ✅ **Armazenamento Persistente Multi-formato**:
  - Ficheiros de texto (`data/logs/game_history.txt`)
  - Ficheiros CSV (`data/metrics/matches.csv`)
  - Ficheiros JSON (`data/config/settings.json` e `leaderboard.json`)
- ✅ **GitHub durante todo o desenvolvimento**: Commits modulares e estruturados.
- ✅ **Documentação Completa**:
  - [Documentação Técnica](docs/DOCUMENTACAO_TECNICA.md)
  - [Manual do Utilizador](docs/MANUAL_UTILIZADOR.md)

---

## ⭐ Elementos de Valorização Implementados

- ⭐ **Interface Gráfica**: NiceGUI moderna, responsiva, com abas e suporte a modo claro/escuro.
- ⭐ **Integração com APIs**: Cliente para a API local do Ollama (`http://localhost:11434`).
- ⭐ **Visualização Gráfica de Dados**: Gráficos dinâmicos com **ECharts** incorporado.
- ⭐ **Base de Dados**: Base de dados relacional **SQLite** (`data/db/tictactoe.db`).
- ⭐ **Funcionalidades de IA**: Personalidades conversacionais da IA (Sarcástico, Amigável, Científico) + comentários das jogadas.
- ⭐ **Testes Automatizados**: Suite com 13 testes unitários cobrindo lógica e persistência.

---

## 📚 Documentação
- Consulte [`docs/DOCUMENTACAO_TECNICA.md`](docs/DOCUMENTACAO_TECNICA.md) para detalhes de arquitetura.
- Consulte [`docs/MANUAL_UTILIZADOR.md`](docs/MANUAL_UTILIZADOR.md) para guia passo a passo de utilização.
