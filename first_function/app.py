import boto3
import json
import os
import datetime
import ast

# Global variables are reused across execution contexts (if available)
session = boto3.Session()
dynamodb = boto3.resource('dynamodb')

# ignore caps

personToEmail = {
    "Uma Bahl": "ubahl@scu.edu"
}

personToNumber = {
    "Uma Bahl": "650-300-9626"
}

def lambda_handler(event, context):

    table = dynamodb.Table('ReimbursementsTable')

    response = {
        "isBase64Encoded": True,
        "statusCode": 0,
        "headers": {"headerName": "headerValue"},
        "body": ""
    }

    body = event["body"]
    body = ast.literal_eval(body)

    # get all the information from the HTTP request

    revent = body["event"]
    rperson = body["person"]
    dateOfPurchase = body["dateOfPurchase"]
    totalAmount = body["totalAmount"]
    description = body["description"]
    other = body["other"]

    try:
        remail = personToEmail[rperson]
    except:
        remail = "not found"

    try:
        rnumber = personToNumber[rperson]
    except:
        remail = "not found"


    item = {
        "ReimbursementSeeker": rperson,
        "DateAdded": str(datetime.datetime.now()),
        "Reimbursed": "no",
        "DateOfPurchase": dateOfPurchase,
        "Email": remail,
        "Phone": rnumber,
        "Event": revent,
        "Description": description,
        "TotalAmount": totalAmount,
        "Other": other
    }

    table.put_item(
        Item=item
    )

    response["statusCode"] = 200
    response["body"] = json.dumps(item)

    return response

