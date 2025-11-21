from utils.logging_config import logger


class PetRepository:
    def __init__(self, db_client):
        self.db = db_client
        logger.info("Создан PetRepository")

    def save_pet_to_db(self, pet_data):
        try:
            if pet_data.get('category'):
                category = pet_data['category']
                self.db.execute("INSERT INTO categories (id, name) VALUES (%s,%s)",
                                (category['id'], category['name']))
            self.db.execute(
                "INSERT INTO pets (id, name, status, category_id) VALUES (%s,%s,%s,%s)",
                (pet_data['id'], pet_data.get('name', 'unknown'), pet_data.get('status', 'unknown'),
                 pet_data['category']['id'] if pet_data.get('category') else None))
            if pet_data.get('tags') and pet_data['tags'] != []:
                for tag in pet_data['tags']:
                    self.db.execute(
                        "INSERT INTO tags (id, name) VALUES (%s, %s)",
                        (tag['id'], tag['name']))
                    self.db.execute("INSERT INTO pet_tags (pet_id, tag_id) VALUES (%s, %s)",
                                    (pet_data['id'], tag['id']))
            if pet_data.get('photoUrls') and pet_data['photoUrls'] != []:
                for photo in pet_data['photoUrls']:
                    self.db.execute("INSERT INTO photo_urls (pet_id, url) VALUES (%s, %s)",
                                    (pet_data['id'], photo))
        except Exception as e:
            logger.error(f"Ошибка:{e}")
            raise

    def get_pet_from_db(self, pet_id):

        results = self.db.execute("""
        SELECT p.id, p.name, p.status,
        c.id as category_id, c.name as category_name,
        ph.url as photo_url,
        t.id as tag_id, t.name as tag_name FROM pets p
        LEFT JOIN categories c ON p.category_id=c.id
        LEFT JOIN pet_tags pt ON p.id=pt.pet_id
        LEFT JOIN tags t ON pt.tag_id=t.id
        LEFT JOIN photo_urls ph ON p.id=ph.pet_id
        WHERE p.id=%s
        """, (pet_id,))
        if not results:
            return {}
        logger.info("Питомец найден")

        main_info = results[0]
        pet_dict = {
            'id': main_info['id'],
            'category': None,
            'name': main_info['name'],
            'photoUrls': [],
            'tags': [],
            'status': main_info['status']}
        if pet_dict['name'] == 'unknown':
            del pet_dict['name']
        if pet_dict['status'] == 'unknown':
            del pet_dict['status']

        if main_info.get('category_id'):
            pet_dict['category'] = {
                'id': main_info['category_id'],
                'name': main_info['category_name']
            }
        else:
            del pet_dict['category']
        pet_dict['tags'] = [{'id': tag_id, 'name': tag_name}
                            for tag_id, tag_name in
                            {(row['tag_id'], row['tag_name'])
                             for row in results if row.get('tag_id')}]
        pet_dict['photoUrls'] = list({row['photo_url'] for row in results
                                      if row.get('photo_url')})
        return pet_dict

    def delete_pet_from_db(self, pet_id):
        self.db.execute("DELETE FROM pets WHERE id=%s", (pet_id,))
