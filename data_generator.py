from faker import Faker
from typing import List, Optional
import random

fake = Faker()

class PetDataGenerator:

    @staticmethod
    def status_generator():
        return random.choice(["available", "sold", "pending"])

    @staticmethod
    def name_generator():
        return fake.first_name()

    @staticmethod
    def id_generator():
        return random.randint(1,1000)

    @staticmethod
    def category_name_generator():
        categories = ["cat", "dog", "lemur", "bird", "fish", "hamster"]
        return {"id": PetDataGenerator.id_generator(),
                "name": random.choice(categories)}

    @staticmethod
    def photo_url_generator():
        return [fake.image_url() for i in range(random.randint(0,6))]

    @staticmethod
    def tags_generator():
        tags = ["puppy", "cute", "kitty", "funny", "rare_breed"]
        return {"id": PetDataGenerator.id_generator(),
                "name": random.choice(tags)}


generator = PetDataGenerator()