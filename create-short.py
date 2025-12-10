# CreateShort.py
import os
import json
import time
import random
import string
import boto3
from botocore.exceptions import ClientError

TABLE_NAME = os.environ.get("TABLE_NAME", "UrlShortener")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

ALPHABET = string.ascii_letters + string.digits  # base62

def gen_short_id(length=6):
    return ''.join(random.choices(ALPHABET, k=length))

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body') or "{}")
        long_url = (body.get('url') or body.get('longUrl') or "").strip()
        if not long_url:
            return {"statusCode":400, "body": json.dumps({"error":"Missing 'url' in body"})}

        # attempt to insert, retry if collision
        for attempt in range(5):
            short_id = gen_short_id(6)
            item = {
                "shortId": short_id,
                "longUrl": long_url,
                "createdAt": str(int(time.time()))
            }
            try:
                table.put_item(
                    Item=item,
                    ConditionExpression="attribute_not_exists(shortId)"
                )
                break
            except ClientError as e:
                if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                    # collision, try again
                    continue
                else:
                    raise

        # return created short URL (you can add custom domain)
        api_base = (event.get('headers') or {}).get('Host') or os.environ.get('API_BASE')
        protocol = "https"  # API Gateway is https
        short_url = f"{protocol}://{api_base}/{short_id}" if api_base else short_id

        return {
            "statusCode": 201,
            "body": json.dumps({"shortId": short_id, "shortUrl": short_url, "longUrl": long_url})
        }

    except Exception as ex:
        return {"statusCode":500, "body": json.dumps({"error": str(ex)})}
