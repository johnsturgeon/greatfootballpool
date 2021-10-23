""" Copies production data to the dev db """
from pymongo import MongoClient

from instance.config import get_config

prod_config = get_config('PRODUCTION')
dev_config = get_config('DEVELOPMENT')

client: MongoClient = MongoClient(
    host=dev_config.MONGO_HOST,
    username=dev_config.MONGO_USERNAME,
    password=dev_config.MONGO_PASSWORD,
    authSource=dev_config.MONGO_DB
)


def copy_prod_to_dev():
    """ Copies the production database to the development"""
    prod_db = client[prod_config.MONGO_DB]
    dev_db = client[dev_config.MONGO_DB]

    prod_cols = prod_db.list_collection_names()
    dev_cols = dev_db.list_collection_names()
    for col in prod_cols:
        if col != 'system.views':
            if col in dev_cols:
                dev_db.drop_collection(col)
            for record in prod_db[col].find({}):
                dev_db[col].insert_one(record)


if __name__ == '__main__':
    copy_prod_to_dev()
