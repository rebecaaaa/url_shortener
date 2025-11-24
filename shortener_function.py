import boto3
import os
import json
import string
import random

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def generate_short_code(length=7):
    """Gera um código aleatório alfanumérico."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def create_link_handler(event, context):
    """
    Cria uma nova URL encurtada.
    Espera um body JSON: {"url": "https://sua-url-longa.com"}
    """
    try:
        body = json.loads(event.get('body', '{}'))
        long_url = body.get('url')
        
        if not long_url:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Nenhuma "url" foi fornecida no body'})
            }
        
        short_code = generate_short_code()
        
        # Salva no DynamoDB
        table.put_item(
            Item={
                'short_code': short_code,
                'long_url': long_url
            }
        )
        
        # Constrói a URL de resposta
        api_id = event['requestContext']['apiId']
        region = os.environ['AWS_REGION']
        stage = event['requestContext']['stage']
        short_url = f"https" + f"://{api_id}.execute-api.{region}.amazonaws.com/{stage}/{short_code}"

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'short_url': short_url,
                'long_url': long_url
            })
        }

    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

def redirect_link_handler(event, context):
    """
    Redireciona um short_code para a URL longa correspondente.
    """
    try:
        short_code = event['pathParameters']['short_code']
        
        response = table.get_item(
            Key={'short_code': short_code}
        )
        
        item = response.get('Item')
        
        if item:
            return {
                'statusCode': 302,
                'headers': {
                    'Location': item['long_url']
                }
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'URL não encontrada'})
            }
            
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}