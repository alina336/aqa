from faker import Faker
import random

fake = Faker()


class PetDataGenerator:

    categories = ["cat", "dog", "lemur", "bird", "fish", "hamster"]
    tags = ["puppy", "cute", "kitty", "funny", "rare_breed"]
    statuses = ["available", "sold", "pending"]

    @staticmethod
    def id_generator():
        return random.randint(1, 1000)

    @staticmethod
    def name_generator():
        return fake.first_name()

    @staticmethod
    def category_generator():
        return {
            "id": PetDataGenerator.id_generator(),
            "name": random.choice(PetDataGenerator.categories)
        }

    @staticmethod
    def photo_urls_generator():
        return [fake.image_url() for _ in range(random.randint(0, 3))]

    @staticmethod
    def tags_generator():
        return [
            {
                "id": PetDataGenerator.id_generator(),
                "name": random.choice(PetDataGenerator.tags)
            }
        ]

    @staticmethod
    def status_generator():
        return random.choice(PetDataGenerator.statuses)

    @staticmethod
    def generate_pet(**overrides):
        data = {
            "id": PetDataGenerator.id_generator(),
            "category": PetDataGenerator.category_generator(),
            "name": PetDataGenerator.name_generator(),
            "photoUrls": PetDataGenerator.photo_urls_generator(),
            "tags": PetDataGenerator.tags_generator(),
            "status": PetDataGenerator.status_generator(),
        }
        data.update(overrides)
        return data
