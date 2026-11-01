# Tic-Tac-Toe AI (Jogo do Galo)

Aplicação modular de Jogo do Galo desenvolvida em Python com interface gráfica NiceGUI, integração com modelo de linguagem local via Ollama e motor de busca Minimax, suportando persistência multi-formato (TXT, CSV, JSON e SQLite).

---

## Requisitos de Sistema

- Python 3.10 ou superior
- Navegador web moderno (Chrome, Edge, Firefox)
- (Opcional) Instalação local do Ollama para inferência de linguagem natural

---

## Instalação e Execução

1. Instalar as dependências do projeto:
   ```powershell
   pip install -r requirements.txt
   ```

2. Iniciar a aplicação:
   ```powershell
   python main.py
   ```

3. Aceder via browser:
   [http://localhost:8080](http://localhost:8080)

4. Executar os testes unitários automatizados:
   ```powershell
   python -m unittest discover -s tests
   ```

---

## Arquitetura e Módulos

- `core/`: Regras do jogo, gestão de estado do tabuleiro e validações.
  - `board.py`: Classe principal `Board`, matriz 3x3 e verificação de condições de término.
  - `exceptions.py`: Hierarquia de exceções personalizadas (`InvalidMoveError`, `PositionOccupiedError`, etc.).
- `ai/`: Motores de decisão para o adversário automático.
  - `ollama_engine.py`: Comunicação com a API REST local do Ollama e parsing de formato estruturado.
  - `minimax.py`: Algoritmo Minimax determinístico com diferentes níveis de dificuldade.
- `storage/`: Persistência de dados poliglota.
  - `persistence.py`: Escrita e leitura estruturada em ficheiros de texto simples (.txt), formato tabular (.csv), configurações (.json) e base de dados relacional SQLite (.db).
- `tests/`: Suite de testes automatizados com cobertura de regras e persistência.
  - `test_board.py`: Testes unitários para a lógica do tabuleiro e exceções.
  - `test_persistence.py`: Testes unitários para as operações de I/O de dados.
- `docs/`: Documentação do projeto.
  - `DOCUMENTACAO_TECNICA.md`: Especificação técnica de arquitetura, fluxo e estruturas de dados.
  - `MANUAL_UTILIZADOR.md`: Manual operacional de utilização do sistema.

---

## Persistência de Dados

- `data/logs/game_history.txt`: Registo descritivo de cada partida finalizada.
- `data/metrics/matches.csv`: Tabela cronológica com identificador, timestamp, vencedor, jogadas e duração.
- `data/config/settings.json`: Preferências do utilizador (modelo, tema, personalidade).
- `data/config/leaderboard.json`: Agregado de vitórias, derrotas e empates.
- `data/db/tictactoe.db`: Base de dados relacional SQLite com registo persistente de partidas.
