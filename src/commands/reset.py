from .base_command import BaseCommannd
from ..dynamodb_evento import DynamoDbEvento

class Reset(BaseCommannd):  
  def execute(self):
    DynamoDbEvento().deleteTable()
    DynamoDbEvento().create_table()