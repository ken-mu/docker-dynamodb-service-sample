from flask import Flask, jsonify, request
import boto3
import datetime
from boto3.dynamodb.conditions import Key, Attr
import json
from decimal import Decimal
import sys
import os

app = Flask(__name__)

dynamodb = None
dynamodb_r = None

table_name = 'iot-test'

@app.route("/sample")
def sample():
    return jsonify({'clientid': 0, 'timestamp': datetime.datetime.now(), 'ph_value': 7.0, 'ph_unit': 'ph', 'do_value': 100, 'do_unit': '%-sat'})

@app.route("/tables")
def tables():
    res = dynamodb.list_tables()
    return jsonify({'tables': res['TableNames']})

@app.route("/measurement/<client_id>/<timestamp>")
def get_measurement(client_id, timestamp):
    response = dynamodb.get_item(
        TableName=table_name,
        Key={
            'clientid': {'N': client_id},
            'timestamp': {'N': timestamp}
        })
    if response.get('Item') is not None:
        return jsonify(response['Item'])
    else:
        return "[]"

def decimal_default_proc(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def get_timestamp_from():
    ts_from = request.args.get('from')
    if ts_from is not None:
        return int(ts_from)
    else:
        return 0

def get_timestamp_to():
    ts_to = request.args.get('to')
    if ts_to is not None:
        return int(ts_to)
    else:
        return sys.maxint

@app.route("/measurements/<int:client_id>")
def get_measurements(client_id):
    table = dynamodb_r.Table(table_name)
    ts_from = get_timestamp_from()
    ts_to = get_timestamp_to()
    response = table.query(
        KeyConditionExpression=Key('clientid').eq(client_id) & Key('timestamp').between(ts_from, ts_to)
    )
    return json.dumps(response['Items'],default=decimal_default_proc)

if __name__ == "__main__":
    if os.environ.get('DYNAMODB_ENDPOINT_URL') is None:
        dynamodb = boto3.client('dynamodb', region_name="ap-northeast-1")
        dynamodb_r = boto3.resource('dynamodb', region_name="ap-northeast-1")
    else:
        dynamodb = boto3.client('dynamodb', region_name="ap-northeast-1", endpoint_url=os.environ['DYNAMODB_ENDPOINT_URL'])
        dynamodb_r = boto3.resource('dynamodb', region_name="ap-northeast-1", endpoint_url=os.environ['DYNAMODB_ENDPOINT_URL'])
    app.run(host='0.0.0.0')
