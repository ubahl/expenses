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
    "Uma Bahl": "ubahl@scu.edu",
    "Tiana Nguyen": "t25nguyen@scu.edu",
    "Matthew Zhang": "mlzhang@scu.edu",
    "Matthew Mistele": "mmistele@scu.edu",
    "Kade Harmon": "kpharmon@scu.edu",
    "Philip Cori": "pcori@scu.edu",
    "Story DeWeese": "sdeweese@scu.edu",
    "Alexander Kennedy": "akennedy2@scu.edu"
}

personToNumber = {
    "Uma Bahl": "650-300-9626",
    "Tiana Nguyen": "408-500-5588",
    "Matthew Zhang": "775-233-7097",
    "Matthew Mistele": "‭425-635-8517‬",
    "Kade Harmon": "925-389-2424",
    "Philip Cori": "669-777-8180",
    "Story DeWeese": "423-596-4294",
    "Alexander Kennedy": "925-915-9124"
}

def lambda_handler(event, context):

    print("event ", event)

    table = dynamodb.Table('ReimbursementsTable')

    response = {
        "isBase64Encoded": True,
        "statusCode": 0,
        "headers": {"headerName": "headerValue"},
        "body": ""
    }

    body = event["body"]

    print("type ", type(body))
    print("body ", body)

    body = json.loads(body)

    print("loads ", body)

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

    print(item)

    response["statusCode"] = 200
    response["body"] = json.dumps(item)

    return response

