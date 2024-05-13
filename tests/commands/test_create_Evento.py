import unittest
from unittest.mock import MagicMock, patch
from src.commands.create_evento import CreateEvento
from src.errors.errors import InvalidNombreError, EventoAlreadyExists, IncompleteParams 
from src.models.evento import Evento
from faker import Faker
import random
from datetime import datetime, timedelta  

class TestCreateEvento(unittest.TestCase):
    def setUp(self):
        '''Crea una instancia de Faker'''
        self.data_factory = Faker()

        '''Se programa para que Faker cree los mismos datos cuando se ejecuta'''
        Faker.seed(1000)
        
        self.lugar = ['Medellín', 'Abejorral', 'Anza']
        self.nivel = ['BASICO','AVANZADO','INTERMEDIO']
        
        
        # Genera una fecha aleatoria igual o mayor a la fecha actual
        fecha_actual = datetime.now()
        fecha_aleatoria = fecha_actual + timedelta(days=random.randint(0, 30))
        
        self.data = {
            'nombre':  self.data_factory.word(),
            'lugar': random.choice(self.lugar),
            'fecha_evento': fecha_aleatoria.strftime('%Y-%m-%d %H:%M:%S'),
            'id_socio': '07adc016-82eb-4c92-b722-0e80ebfdcfe5',
            'descripcion': self.data_factory.text(),
            'nivel': random.choice(self.nivel),
            'estado': random.choice([True, False])
        }
    
        self.create_evento = CreateEvento(self.data)
    
    def tearDown(self):
        # Restablecer los mocks
        patch.stopall()
        
        pass

    @patch('src.commands.create_evento.DynamoDbEvento')
    def test_crear_evento(self, mock_dynamodb_evento):
        '''1.Crea un nuevo evento'''
        mock_dynamodb_evento_instance = mock_dynamodb_evento.return_value
        mock_dynamodb_evento_instance.get_Item_nombre.return_value = None
        mock_dynamodb_evento_instance.insert_item.return_value = None

        resultado = self.create_evento.execute()

        self.assertIsInstance(resultado, Evento)
        mock_dynamodb_evento_instance.insert_item.assert_called_once()

    @patch('src.commands.create_evento.DynamoDbEvento')
    def test_evento_existente(self, mock_dynamodb_evento):
        '''2.Crea un nuevo evento con el mismo nombre de un evento existente'''
        mock_dynamodb_evento_instance = mock_dynamodb_evento.return_value
        mock_dynamodb_evento_instance.get_Item_nombre.return_value = {'nombre': self.data['nombre']}

        with self.assertRaises(EventoAlreadyExists):
            self.create_evento.execute()

    def test_nombre_invalido(self):
            '''3.Crea un nuevo evento con nombre invalido'''
            data_invalida = self.data.copy()
            data_invalida['nombre'] = ''

            create_evento_invalido = CreateEvento(data_invalida)

            with self.assertRaises(InvalidNombreError):
                create_evento_invalido.execute()

    @patch('src.commands.create_evento.Evento')
    def test_datos_incompletos(self, mock_evento):
        '''4.Simular un TypeError al crear la instancia de Evento'''
        # Simular un TypeError al crear la instancia de Evento
        mock_evento.side_effect = TypeError('Error de tipo en la creación de Evento')

        with self.assertRaises(IncompleteParams):
            self.create_evento.execute()

    if __name__ == '__main__':
        unittest.main()