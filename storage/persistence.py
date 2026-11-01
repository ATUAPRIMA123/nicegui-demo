"""
Módulo de Armazenamento Persistente Multi-formato
Implementa a gravação e leitura de dados utilizando:
1. Ficheiros de Texto (.txt) - Registo narrativo de partidas
2. Ficheiros CSV (.csv) - Base de dados tabular para análise métrica
3. Ficheiros JSON (.json) - Configurações e perfis/classificação
4. Base de Dados SQLite (.db) - Persistência relacional avançada (Elemento de Valorização)
"""

import os
import csv
import json
import sqlite3
from datetime import datetime
from typing import Dict, Any, List, Optional

from core.exceptions import StorageError


class StorageManager:
    """Gere as operações de I/O em múltiplos formatos com validação e tolerância a falhas."""

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    TXT_PATH = os.path.join(DATA_DIR, 'logs', 'game_history.txt')
    CSV_PATH = os.path.join(DATA_DIR, 'metrics', 'matches.csv')
    CONFIG_PATH = os.path.join(DATA_DIR, 'config', 'settings.json')
    LEADERBOARD_PATH = os.path.join(DATA_DIR, 'config', 'leaderboard.json')
    DB_PATH = os.path.join(DATA_DIR, 'db', 'tictactoe.db')

    CSV_HEADERS = [
        'match_id', 'timestamp', 'player_name', 'winner',
        'total_moves', 'difficulty', 'ai_engine', 'duration_seconds'
    ]

    def __init__(self):
        self._ensure_directories()
        self._init_csv()
        self._init_database()

    def _ensure_directories(self) -> None:
        """Garante a existência de todas as pastas necessárias."""
        for path in [
            os.path.dirname(self.TXT_PATH),
            os.path.dirname(self.CSV_PATH),
            os.path.dirname(self.CONFIG_PATH),
            os.path.dirname(self.DB_PATH),
        ]:
            os.makedirs(path, exist_ok=True)

    # ==========================================
    # 1. ARMAZENAMENTO EM FICHEIROS DE TEXTO (.TXT)
    # ==========================================
    def append_text_log(self, match_data: Dict[str, Any]) -> None:
        """Adiciona uma entrada narrativa formatada ao ficheiro de texto."""
        try:
            timestamp = match_data.get('timestamp', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            player = match_data.get('player_name', 'Jogador')
            winner = match_data.get('winner', 'DRAW')
            engine = match_data.get('ai_engine', 'Minimax')
            moves = match_data.get('total_moves', 0)

            result_str = "Empate" if winner == 'DRAW' else f"Vitória de {winner} ({player if winner == 'X' else 'IA'})"

            entry = (
                f"[{timestamp}] PARTIDA #{match_data.get('match_id', 'N/A')}\n"
                f"  Jogador: {player} (X) vs IA ({engine}) (O)\n"
                f"  Resultado: {result_str}\n"
                f"  Total de Jogadas: {moves}\n"
                f"  Duração: {match_data.get('duration_seconds', 0)}s\n"
                f"{'-'*50}\n"
            )

            with open(self.TXT_PATH, 'a', encoding='utf-8') as f:
                f.write(entry)
        except Exception as e:
            raise StorageError(self.TXT_PATH, f"Erro ao escrever log TXT: {e}")

    def read_text_logs(self, max_lines: int = 100) -> str:
        """Lê os últimos registos do ficheiro de texto."""
        if not os.path.exists(self.TXT_PATH):
            return "Nenhum histórico registado ainda."
        try:
            with open(self.TXT_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return "".join(lines[-max_lines:])
        except Exception as e:
            raise StorageError(self.TXT_PATH, f"Erro ao ler log TXT: {e}")

    # ==========================================
    # 2. ARMAZENAMENTO EM CSV (.CSV)
    # ==========================================
    def _init_csv(self) -> None:
        """Cria o ficheiro CSV com cabeçalhos caso ainda não exista."""
        if not os.path.exists(self.CSV_PATH):
            try:
                with open(self.CSV_PATH, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(self.CSV_HEADERS)
            except Exception as e:
                raise StorageError(self.CSV_PATH, f"Erro ao inicializar CSV: {e}")

    def append_csv_record(self, match_data: Dict[str, Any]) -> None:
        """Insere uma linha com as métricas da partida no CSV."""
        try:
            row = [
                match_data.get('match_id', ''),
                match_data.get('timestamp', datetime.now().isoformat()),
                match_data.get('player_name', 'Jogador'),
                match_data.get('winner', 'DRAW'),
                match_data.get('total_moves', 0),
                match_data.get('difficulty', 'Imbatível'),
                match_data.get('ai_engine', 'Minimax'),
                match_data.get('duration_seconds', 0)
            ]
            with open(self.CSV_PATH, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(row)
        except Exception as e:
            raise StorageError(self.CSV_PATH, f"Erro ao gravar no CSV: {e}")

    def read_csv_records(self) -> List[Dict[str, Any]]:
        """Lê todos os registos do ficheiro CSV em formato de lista de dicionários."""
        if not os.path.exists(self.CSV_PATH):
            return []
        try:
            records = []
            with open(self.CSV_PATH, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append(row)
            return records
        except Exception as e:
            raise StorageError(self.CSV_PATH, f"Erro ao ler CSV: {e}")

    # ==========================================
    # 3. ARMAZENAMENTO EM JSON (.JSON)
    # ==========================================
    def load_settings(self) -> Dict[str, Any]:
        """Carrega as configurações salvas em JSON com valores padrão seguros."""
        defaults = {
            'player_name': 'Jogador',
            'ollama_model': 'llama3.2',
            'ollama_host': 'http://localhost:11434',
            'personality': 'Sarcástico',
            'difficulty': 'Imbatível',
            'dark_mode': False,
        }
        if not os.path.exists(self.CONFIG_PATH):
            self.save_settings(defaults)
            return defaults
        try:
            with open(self.CONFIG_PATH, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                defaults.update(saved)
                return defaults
        except Exception as e:
            # Em caso de ficheiro corrompido, retorna defaults
            return defaults

    def save_settings(self, settings: Dict[str, Any]) -> None:
        """Guarda as configurações em formato JSON."""
        try:
            with open(self.CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise StorageError(self.CONFIG_PATH, f"Erro ao gravar settings.json: {e}")

    def update_leaderboard(self, winner: str) -> Dict[str, int]:
        """Atualiza e persiste o placar acumulado em JSON."""
        stats = {'player_wins': 0, 'ai_wins': 0, 'draws': 0, 'total_games': 0}
        if os.path.exists(self.LEADERBOARD_PATH):
            try:
                with open(self.LEADERBOARD_PATH, 'r', encoding='utf-8') as f:
                    stats.update(json.load(f))
            except Exception:
                pass

        stats['total_games'] += 1
        if winner == 'X':
            stats['player_wins'] += 1
        elif winner == 'O':
            stats['ai_wins'] += 1
        else:
            stats['draws'] += 1

        try:
            with open(self.LEADERBOARD_PATH, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=4)
        except Exception as e:
            raise StorageError(self.LEADERBOARD_PATH, f"Erro ao atualizar leaderboard.json: {e}")

        return stats

    def get_leaderboard(self) -> Dict[str, int]:
        """Lê o placar acumulado em JSON."""
        stats = {'player_wins': 0, 'ai_wins': 0, 'draws': 0, 'total_games': 0}
        if os.path.exists(self.LEADERBOARD_PATH):
            try:
                with open(self.LEADERBOARD_PATH, 'r', encoding='utf-8') as f:
                    stats.update(json.load(f))
            except Exception:
                pass
        return stats

    # ==========================================
    # 4. BASE DE DADOS SQLITE (.DB) (VALORIZAÇÃO)
    # ==========================================
    def _init_database(self) -> None:
        """Inicializa as tabelas da base de dados relacional SQLite."""
        try:
            with sqlite3.connect(self.DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS matches (
                        id TEXT PRIMARY KEY,
                        timestamp TEXT NOT NULL,
                        player_name TEXT NOT NULL,
                        winner TEXT NOT NULL,
                        total_moves INTEGER NOT NULL,
                        difficulty TEXT NOT NULL,
                        ai_engine TEXT NOT NULL,
                        duration_seconds REAL NOT NULL
                    )
                """)
                conn.commit()
        except Exception as e:
            raise StorageError(self.DB_PATH, f"Erro ao inicializar base de dados SQLite: {e}")

    def insert_db_match(self, match_data: Dict[str, Any]) -> None:
        """Insere a partida na base de dados SQLite."""
        try:
            with sqlite3.connect(self.DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO matches (
                        id, timestamp, player_name, winner, total_moves, difficulty, ai_engine, duration_seconds
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(match_data.get('match_id', '')),
                    str(match_data.get('timestamp', datetime.now().isoformat())),
                    str(match_data.get('player_name', 'Jogador')),
                    str(match_data.get('winner', 'DRAW')),
                    int(match_data.get('total_moves', 0)),
                    str(match_data.get('difficulty', 'Imbatível')),
                    str(match_data.get('ai_engine', 'Minimax')),
                    float(match_data.get('duration_seconds', 0.0))
                ))
                conn.commit()
        except Exception as e:
            raise StorageError(self.DB_PATH, f"Erro ao registar na base de dados SQLite: {e}")

    # ==========================================
    # OPERAÇÃO GLOBAL DE PERSISTÊNCIA
    # ==========================================
    def record_match_all_formats(self, match_data: Dict[str, Any]) -> Dict[str, int]:
        """
        Regista uma partida concluída em TODOS os formatos requeridos:
        - TXT, CSV, JSON e SQLite simultaneamente.
        """
        self.append_text_log(match_data)
        self.append_csv_record(match_data)
        self.insert_db_match(match_data)
        return self.update_leaderboard(match_data.get('winner', 'DRAW'))
