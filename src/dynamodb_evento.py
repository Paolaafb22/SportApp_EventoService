import boto3
import os
import json
from boto3.dynamodb.conditions import Key, Attr
#from .models.entrenamiento import Entrenamiento
from .models.evento import Evento
from botocore.exceptions import ClientError

class DynamoDbEvento():
    def __init__(self):        
        # Crear una instancia de cliente DynamoDB
        self.dynamodb = boto3.client('dynamodb',
                                region_name='us-east-1',
                                aws_access_key_id= os.environ['AWS_ACCESS_KEY_ID'],
                                aws_secret_access_key= os.environ['AWS_SECRET_ACCESS_KEY'])
        self.table_name = 'evento'

    # Funciones para interactuar con DynamoDB
    def create_table(self):
        if not self.tablaExits(self.table_name):

            self.dynamodb.create_table(
                    TableName=self.table_name,
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'id_evento',
                            'AttributeType': 'S',
                        }
                    ],
                    KeySchema=[
                        {
                            'AttributeName': 'id_evento',
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

    def insert_item(self,evento: Evento):
        item = {
            "id_evento": {'S':  evento.id_evento },
            'nombre': {'S': evento.nombre },
            'lugar': {'S': evento.lugar },
            'fecha_evento': {'S': evento.fecha_evento},  # Datetime conversion
            'id_socio': {'S': evento.id_socio },
            'descripcion': {'S': evento.descripcion },
            'nivel': {'S': evento.nivel },
            'estado': {'BOOL': evento.estado }
            # Puedes agregar más atributos según la definición de tu tabla
        }
        result = self.dynamodb.put_item(
            TableName=self.table_name,
            Item=item,
            ReturnConsumedCapacity='TOTAL'
        )
        print('Ítem insertado correctamente.')

    def get_item(self,id_evento):
        key = {
            'id_evento': {'S': str(id_evento) }  # Clave de búsqueda
        }
        response = self.dynamodb.get_item(
            TableName=self.table_name,
            Key=key
        )
        item = response.get('Item')
        if not item:
            return None
        
        # Extrae los valores de cada campo
        id_evento = item['id_evento']['S']
        nombre = item['nombre']['S']
        lugar = item['lugar']['S']
        fecha_evento = item['fecha_evento']['S']
        id_socio = item['id_socio']['S']
        descripcion = item['descripcion']['S']
        nivel = item['nivel']['S']
        estado = item['estado']['BOOL']

        # Crea una instancia de la clase Entrenamiento
        evento = Evento(id_evento,nombre, lugar, fecha_evento, id_socio,descripcion,nivel, estado)

        return evento

    def get_Item_nombre(self,nombre):
        
        # Parámetros para la operación de escaneo
        parametros = {
            'TableName': self.table_name,
            'FilterExpression': '#nombre = :nombre',
            'ExpressionAttributeNames': {
                '#nombre': 'nombre'
            },
            'ExpressionAttributeValues': {
                ':nombre': {'S': nombre}
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
            id_evento = item['id_evento']['S']
            nombre = item['nombre']['S']
            lugar = item['lugar']['S']
            fecha_evento = item['fecha_evento']['S']
            id_socio = item['id_socio']['S']
            descripcion = item['descripcion']['S']
            nivel = item['nivel']['S']
            estado = item['estado']['BOOL']
    

            evento = Evento(id_evento,nombre, lugar, fecha_evento, id_socio,descripcion,nivel, estado)
            resultados.append(evento)

        return resultados

    def recomendar_items(self,ciudad,fecha_prevista):
        # Parámetros para la operación de escaneo
        parametros = {
            'TableName': self.table_name,
            'FilterExpression': '#lugar = :lugar',
            'ExpressionAttributeNames': {
                '#lugar': 'lugar'
            },
            'ExpressionAttributeValues': {
                ':lugar': {'S': ciudad}
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
            id_evento = item['id_evento']['S']
            nombre = item['nombre']['S']
            lugar = item['lugar']['S']
            fecha_evento = item['fecha_evento']['S']
            id_socio = item['id_socio']['S']
            descripcion = item['descripcion']['S']
            nivel = item['nivel']['S']
            estado = item['estado']['BOOL']
    

            evento = Evento(id_evento,nombre, lugar, fecha_evento, id_socio,descripcion,nivel, estado)
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