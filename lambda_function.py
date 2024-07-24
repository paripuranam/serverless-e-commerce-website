import json
import boto3
from datetime import datetime
import logging

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        if 'body' not in event:
            raise KeyError('body')
        
        body = json.loads(event['body'])
        product_name = body['productName']
        quantity = body['quantity']
        price = body['price']

        table.put_item(
            Item={
                'orderId': str(datetime.utcnow().timestamp()),
                'productName': product_name,
                'quantity': quantity,
                'price': price
            }
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps('Order placed successfully!')
        }
        
    except KeyError as e:
        logger.error(f"KeyError: {str(e)}")
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(f"Missing key: {str(e)}")
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps("Internal server error")
        }
