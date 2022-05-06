import json

import boto3
import nacl.pwhash

from data import LabeledImage, User

# I will assume the credentials are set up correctly inside creds.json
with open("creds.json") as f:
    creds = json.load(f)
ddb = boto3.resource("dynamodb", region_name="us-east-1",
                     aws_access_key_id=creds["aws_access_key_id"],
                     aws_secret_access_key=creds["aws_secret_access_key"])

users = ddb.Table("Reduce_users")
images = ddb.Table("Reduce_images")


def add_user(user: User):
    users.put_item(
        Item=user.to_dict()
    )


def get_user(user_email: str) -> User:
    res = users.get_item(Key={"email": user_email})
    # User does not exist
    if "Item" not in res:
        return None
    item = res["Item"]

    return User(item["email"], item["first_name"], item["last_name"], item["password_hash"])


def add_img_to_user(user: User, image: LabeledImage):
    # Local changes
    users.image_ids.append(image.image_id)

    # Add stuff to db tables

    # Upload image
    images.put_item(
        Item=image.to_dict()
    )
    # Append image id to user entry
    users.update_item(
        Key={
            "email": user.email,
        },
        UpdateExpression="SET image_ids = list_append(image_ids, :img_ids)",
        ExpressionAttributeValues={
            ":img_ids": [image.image_id]
        }
    )
