# RedirectShort.py
import os
import json
import boto3

TABLE_NAME = os.environ.get("TABLE_NAME", "UrlShortener")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    try:
        path_params = event.get('pathParameters') or {}
        short_id = path_params.get('shortId') or path_params.get('id')
        if not short_id:
            return {"statusCode":400, "body": json.dumps({"error":"Missing shortId in path"})}

        resp = table.get_item(Key={"shortId": short_id})
        item = resp.get('Item')
        if not item:
            return {"statusCode":404, "body": json.dumps({"error":"Short URL not found"})}

        long_url = item['longUrl']
        return {
            "statusCode": 302,
            "headers": {"Location": long_url},
            "body": ""
        }
    except Exception as ex:
        return {"statusCode":500, "body": json.dumps({"error": str(ex)})}
