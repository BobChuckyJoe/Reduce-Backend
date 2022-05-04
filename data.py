class User:
    def __init__(self, email, first_name, last_name, password_hash):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = password_hash

        # Information about user specific data
        self.image_ids = []
        self.plastic_bottles = 0
    
    def to_dict(self):
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password_hash": self.password_hash,
            "image_ids": self.image_ids,
            "plastic_bottles": self.plastic_bottles
        }

# Contains an item that has bounding boxes for each bottle
class LabeledImage:
    def __init__(self, image_id, date_time, raw_img_data):
        self.image_id = image_id
        # In unix epoch time
        self.date_time = date_time
        # Base64 encode this
        self.raw_img_data = raw_img_data

        # Calculate this data
        self.annotated_image = None
        self.num_bottles = 0

    def to_dict(self):
        return {
            "image_id": self.image_id,
            "date_time": self.date_time,
            "annotated_image": self.annotated_image,
            "num_bottles": self.num_bottles
        }
    