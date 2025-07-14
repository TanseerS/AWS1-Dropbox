import json
import boto3
import uuid
import os
import datetime

s3_client = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
bucket_name = os.environ["BUCKET_NAME"]
table = dynamodb.Table(os.environ["TABLE_NAME"])
cdn_domain = os.environ.get("CLOUDFRONT_DOMAIN")

def lambda_handler(event, context):
    method = event["requestContext"]["http"]["method"]
    path = event["requestContext"]["http"]["path"]
    query = event.get("queryStringParameters") or {}
    body = json.loads(event.get("body") or "{}")

    try:
        if method == "GET" and path.endswith("/upload"):
            filename = query.get("name")
            if not filename:
                return respond(400, {"error": "Missing filename"})

            file_id = str(uuid.uuid4())
            key = f"{file_id}.{filename.split('.')[-1]}"

            table.put_item(Item={
                "file_id": file_id,
                "filename": filename,
                "s3_key": key,
                "upload_status": "PENDING",
                "created_at": datetime.datetime.utcnow().isoformat()
            })

            url = s3_client.generate_presigned_url(
                ClientMethod="put_object",
                Params={"Bucket": bucket_name, "Key": key},
                ExpiresIn=3600
            )
            return respond(200, {"fileId": file_id, "uploadURL": url})

        elif method == "GET" and path.endswith("/download"):
            file_id = query.get("fileId")
            if not file_id:
                return respond(400, {"error": "Missing fileId"})

            item = table.get_item(Key={"file_id": file_id}).get("Item")
            if not item:
                return respond(404, {"error": "File not found"})

            key = item["s3_key"]
            url = s3_client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": bucket_name, "Key": key},
                ExpiresIn=3600
            )
            response = {"downloadURL": url}
            if cdn_domain:
                response["cdnURL"] = f"https://{cdn_domain}/{key}"
            return respond(200, response)

        elif method == "GET" and path.endswith("/multipart"):
            filename = query.get("name")
            parts = int(query.get("parts", "1"))
            if not filename or parts < 1:
                return respond(400, {"error": "Missing filename or invalid parts"})

            file_id = str(uuid.uuid4())
            key = f"{file_id}.{filename.split('.')[-1]}"

            upload = s3_client.create_multipart_upload(Bucket=bucket_name, Key=key)
            upload_id = upload["UploadId"]

            urls = []
            for i in range(1, parts + 1):
                url = s3_client.generate_presigned_url(
                    ClientMethod="upload_part",
                    Params={
                        "Bucket": bucket_name,
                        "Key": key,
                        "UploadId": upload_id,
                        "PartNumber": i
                    },
                    ExpiresIn=3600
                )
                urls.append(url)

            table.put_item(Item={
                "file_id": file_id,
                "filename": filename,
                "s3_key": key,
                "upload_id": upload_id,
                "upload_status": "MULTIPART_IN_PROGRESS",
                "created_at": datetime.datetime.utcnow().isoformat()
            })

            return respond(200, {
                "fileId": file_id,
                "uploadId": upload_id,
                "partUploadURLs": urls
            })

        elif method == "POST" and path.endswith("/complete"):
            file_id = body.get("fileId")
            upload_id = body.get("uploadId")
            parts = body.get("parts", [])

            item = table.get_item(Key={"file_id": file_id}).get("Item")
            if not item or item.get("upload_id") != upload_id:
                return respond(400, {"error": "Invalid fileId or uploadId"})

            key = item["s3_key"]
            sorted_parts = sorted(parts, key=lambda x: x["PartNumber"])
            for part in sorted_parts:
                part["ETag"] = part["ETag"].strip('"')

            s3_client.complete_multipart_upload(
                Bucket=bucket_name,
                Key=key,
                UploadId=upload_id,
                MultipartUpload={"Parts": sorted_parts}
            )
            return respond(200, {"message": "Multipart upload completed"})

        else:
            return respond(404, {"error": "Unsupported route"})

    except Exception as e:
        return respond(500, {"error": str(e)})

def respond(status, body):
    return {
        "statusCode": status,
        "body": json.dumps(body),
        "headers": {"Content-Type": "application/json"}
    }
