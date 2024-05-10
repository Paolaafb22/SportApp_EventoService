import unittest
from unittest.mock import MagicMock, patch
from src.commands.get_evento import GetEvento
from src.commands.get_All_evento import GetAllEvento
from src.errors.errors import IncompleteParams, InvalidNombreError,Unauthorized, InvalidParams, EventoNotFoundError
from src.dynamodb_evento import DynamoDbEvento

class TestGetEvento(unittest.TestCase):
    def test_prueba(self):
            self.assertEqual(0, 0)
    