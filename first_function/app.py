import boto3
import json
import os
import datetime
import ast
from urllib.parse import parse_qs

# Global variables are reused across execution contexts (if available)
session = boto3.Session()
dynamodb = boto3.resource('dynamodb')
sesclient = boto3.client('ses')

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

    tablename = os.environ['TABLE_NAME']
    table = dynamodb.Table(tablename)

    response = {
        "isBase64Encoded": True,
        "statusCode": 0,
        "headers": {"Access-Control-Allow-Origin": "http://umabahl.com"},
        "body": ""
    }

    body = event["body"]

    print("type ", type(body))
    print("body ", body)

    body = parse_qs(body)

    print("parsed ", body)

    # get all the information from the HTTP request
    if len(body) < 5:
        response["statusCode"] = 200
        response["body"] = "invalid attempt"
        return response

    revent = body["event"][0]
    rperson = body["person"][0]
    dateOfPurchase = body["dateOfPurchase"][0]
    totalAmount = body["totalAmount"][0]
    description = body["desciption"][0]

    try:
        other = body["other"][0]
    except:
        other = "no other details"

    try:
        remail = personToEmail[rperson]
    except:
        remail = "not found"

    try:
        rnumber = personToNumber[rperson]
    except:
        rnumber = "not found"

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
    response["body"] = "Your response has been recorded. Here is the information Uma Bahl Reimbursement Co. has received: \n {}".format(item)
    sendemail(item)

    return response


def sendemail(item):
    response = sesclient.send_email(
        Source="reimbursement@umabahl.com",
        Destination={
            "ToAddresses": [
                "ubahl@scu.edu",
                item["Email"]
            ]
        },
        Message={
            "Subject": {
                "Data": "Summary of Your Reimbursement"
            },
            "Body": {
                "Text": {
                    "Data": ("Dear {}, \n \n"
                             "Here is a summary of your recent reimbursement: \n \n"
                             "Total Amount: {} \n"
                             "Event: {} \n"
                             "Description: {} \n"
                             "Date of Purchase: {} \n"
                             "Other: {} \n \n"
                             "Don't forget to send a copy of the receipt! \n \n"
                             "Best, \n"
                             "Your Neighborhood Treasurer"
                             ).format(item["ReimbursementSeeker"], item["TotalAmount"], item["Event"], item["Description"], item["DateOfPurchase"], item["Other"])
                }
            }
        },
        # SourceArn=os.environ['POLICY_ARN']
    )

    print(response)



