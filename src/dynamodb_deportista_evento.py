import boto3
import os
import json
from boto3.dynamodb.conditions import Key, Attr
from .models.deportista_evento import DeportistaEvento
from botocore.exceptions import ClientError

class DynamoDbDeportistaEvento():
    def __init__(self):        
        # Crear una instancia de cliente DynamoDB
        self.dynamodb = boto3.client('dynamodb',
                                region_name='us-east-1',
                                aws_access_key_id= os.environ['AWS_ACCESS_KEY_ID'],
                                aws_secret_access_key= os.environ['AWS_SECRET_ACCESS_KEY'])
        self.table_name = 'deportista-evento'

    # Funciones para interactuar con DynamoDB
    def create_table(self):
        if not self.tablaExits(self.table_name):

            self.dynamodb.create_table(
                    TableName=self.table_name,
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'id_usuario_evento',
                            'AttributeType': 'S',
                        }
                    ],
                    KeySchema=[
                        {
                            'AttributeName': 'id_usuario_evento',
                            'KeyType': 'HASH'  # Clave de partición
                        }
                    ],        
                    ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5,
                    } 
                )
            
            # Espera hasta que la tabla exista
            self.dynamodb.get_waiter('table_exists').wait(TableName=self.table_name)
            print(f'Tabla {self.table_name} creada correctamente.')
        else:
            print(f"La tabla '{self.table_name}' ya existe.")

    def insert_item(self,evento_deportista: DeportistaEvento):
        item = {
            "id_usuario_evento":{'S': evento_deportista.id_usuario_evento},
            "id_usuario": {'S':  evento_deportista.id_usuario  },
            'id_evento': {'S': evento_deportista.id_evento  },
            'fecha_suscripcion': {'S': evento_deportista.fecha_suscripcion},
            'estado_suscripcion': {'BOOL': evento_deportista.estado_suscripcion }
            # Puedes agregar más atributos según la definición de tu tabla
        }
        result = self.dynamodb.put_item(
            TableName=self.table_name,
            Item=item,
            ReturnConsumedCapacity='TOTAL'
        )
        print('Ítem insertado correctamente.')

    def get_Item_usuario(self,id_usuario):
        
        # Parámetros para la operación de escaneo
        parametros = {
            'TableName': self.table_name,
            'FilterExpression': '#id_usuario = :id_usuario',
            'ExpressionAttributeNames': {
                '#id_usuario': 'id_usuario'
            },
            'ExpressionAttributeValues': {
                ':id_usuario': {'S': id_usuario}
            }
        }
    
        # Realizar el escaneo
        response = self.dynamodb.scan(**parametros)
        print(response)
        # Obtener los items encontrados
        items = response.get('Items', [])
        if not items:
            return None
        
        # Procesar los items encontrados
        resultados = []
        for item in items:
            id_usuario_evento = item['id_usuario_evento']['S']
            id_usuario = item['id_usuario']['S']
            id_evento = item['id_evento']['S']
            fecha_suscripcion = item['fecha_suscripcion']['S']
            estado_suscripcion = item['estado_suscripcion']['BOOL']    

            evento = DeportistaEvento(id_usuario_evento,id_usuario,id_evento, fecha_suscripcion, estado_suscripcion)
            resultados.append(evento)

        return resultados
    
    def exit_event_usuario(self, id_usuario, id_evento):
        # Parámetros para la operación de escaneo
        parametros = {
            'TableName': self.table_name,
            'FilterExpression': '#id_usuario = :id_usuario AND #id_evento = :id_evento',
            'ExpressionAttributeNames': {
                '#id_usuario': 'id_usuario',
                '#id_evento': 'id_evento'
            },
            'ExpressionAttributeValues': {
                ':id_usuario': {'S': id_usuario},
                ':id_evento': {'S': id_evento}
            }
        }
    
        # Realizar el escaneo
        response = self.dynamodb.scan(**parametros)
        print(response)
        # Obtener los items encontrados
        items = response.get('Items', [])
        if not items:
            return None
        
        # Procesar los items encontrados
        resultados = []
        for item in items:
            id_usuario_evento = item['id_usuario_evento']['S']
            id_usuario = item['id_usuario']['S']
            id_evento = item['id_evento']['S']
            fecha_suscripcion = item['fecha_suscripcion']['S']
            estado_suscripcion = item['estado_suscripcion']['BOOL']    

            evento = DeportistaEvento(id_usuario_evento, id_usuario,id_evento, fecha_suscripcion, estado_suscripcion)
            resultados.append(evento)

        return resultados
    
    def tablaExits(self,name):
        try:
            response = self.dynamodb.describe_table(TableName=name)
            print(response)
            return True
        except ClientError as err:
            print(f"Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
            if err.response['Error']['Code'] == 'ResourceNotFoundException':
                return False

    def deleteTable(self):
        # Eliminar la tabla
        self.dynamodb.delete_table(TableName=self.table_name)

        # Esperar hasta que la tabla no exista
        self.dynamodb.get_waiter('table_not_exists').wait(TableName=self.table_name)