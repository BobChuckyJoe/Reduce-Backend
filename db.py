import boto3

from data import User
# I will assume the credentials are set up correctly
ddb = boto3.resource("dynamodb")

users = ddb.Table("Reduce_users")
images = ddb.Table("Reduce_images")

def add_user(user: User):
    users.put_item(
        Item=user.to_dict()
    )

def get_user(user_email):
    res = users.get_item(Key= {"email": user_email})
    return res["Item"]

def add_img_to_user(user: User, image: Image):
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
            "email":user.email,
        },
        UpdateExpression="SET image_ids = list_append(image_ids, :img_ids)",
        ExpressionAttributeValues={
            ":img_ids": [image.image_id]
        }
    )
