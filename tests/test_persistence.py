"""
Testes Automatizados para a Persistência Multi-formato (StorageManager)
Testa gravação e leitura de TXT, CSV, JSON e SQLite.
"""

import unittest
import os
import shutil
from storage.persistence import StorageManager


class TestPersistence(unittest.TestCase):
    def setUp(self):
        self.storage = StorageManager()
        self.sample_match = {
            'match_id': 'TEST_001',
            'timestamp': '2026-11-01 20:00:00',
            'player_name': 'TestUser',
            'winner': 'X',
            'total_moves': 5,
            'difficulty': 'Imbatível',
            'ai_engine': 'Minimax',
            'duration_seconds': 12.5
        }

    def test_txt_logging(self):
        """Testa adição e leitura do registo de texto."""
        self.storage.append_text_log(self.sample_match)
        logs = self.storage.read_text_logs()
        self.assertIn("PARTIDA #TEST_001", logs)
        self.assertIn("TestUser", logs)

    def test_csv_persistence(self):
        """Testa inserção e leitura no formato CSV."""
        self.storage.append_csv_record(self.sample_match)
        records = self.storage.read_csv_records()
        self.assertTrue(len(records) > 0)
        found = any(r.get('match_id') == 'TEST_001' for r in records)
        self.assertTrue(found)

    def test_json_leaderboard_update(self):
        """Testa a atualização do placar JSON."""
        stats = self.storage.update_leaderboard('X')
        self.assertIn('player_wins', stats)
        self.assertGreaterEqual(stats['player_wins'], 1)

    def test_sqlite_insert(self):
        """Testa a inserção na base de dados SQLite."""
        self.storage.insert_db_match(self.sample_match)
        import sqlite3
        with sqlite3.connect(self.storage.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, player_name FROM matches WHERE id = 'TEST_001'")
            row = cursor.fetchone()
            self.assertIsNotNone(row)
            self.assertEqual(row[1], 'TestUser')


if __name__ == '__main__':
    unittest.main()
