import boto3
import os
import json
import datetime

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")
sns = boto3.client("sns")

table = dynamodb.Table(os.environ["TABLE_NAME"])
topic_arn = os.environ["TOPIC_ARN"]

def lambda_handler(event, context):
    for record in event["Records"]:
        if record["eventName"].startswith("ObjectCreated:"):
            bucket = record["s3"]["bucket"]["name"]
            key = record["s3"]["object"]["key"]
            size = record["s3"]["object"].get("size", 0)

            file_id = key.split(".")[0]
            try:
                item = table.get_item(Key={"file_id": file_id}).get("Item")
                if not item:
                    print(f"Item not found for file_id {file_id}")
                    continue

                table.update_item(
                    Key={"file_id": file_id},
                    UpdateExpression="SET upload_status = :s, file_size = :z, completed_at = :t",
                    ExpressionAttributeValues={
                        ":s": "COMPLETED",
                        ":z": size,
                        ":t": datetime.datetime.utcnow().isoformat()
                    }
                )

                filename = item.get("filename", key)
                msg = f"File '{filename}' (ID: {file_id}) of size {size} bytes was uploaded."
                sns.publish(
                    TopicArn=topic_arn,
                    Subject="File Upload Completed",
                    Message=msg
                )
                print(f"Notification sent for {file_id}")
            except Exception as e:
                print(f"Error processing {file_id}: {str(e)}")

    return {"statusCode": 200}
