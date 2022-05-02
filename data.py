class User:
    def __init__(self, email, first_name, last_name, salt, password_hash):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.salt = salt
        self.password_hash = password_hash

        # Information about user specific data
        self.image_ids = []
        self.plastic_bottles = 0
    
    def to_dict(self):
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last,
            "salt": self.salt,
            "password_hash": self.password_hash,
            "image_ids": self.image_ids
        }

class Image:
    def __init__(self, image_id, date_time, img_data):
        self.image_id = image_id
        # In unix epoch time
        self.date_time = date_time
        # Base64 encode this
        self.img_data = img_data

    def to_dict(self):
        return {
            "image_id": self.image_id,
            "date_time": self.date_time,
            "img_data": self.img_data
        }
    