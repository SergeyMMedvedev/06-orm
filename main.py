import sqlalchemy as sq
import os
import json
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
from sqlalchemy.exc import NoResultFound


class Fixtures:

    @classmethod
    def get_fixtures(cls, path):
        with open(path) as f:
            fixtures = json.load(f)
        return fixtures

    def __init__(self, path):
        self._fixtures = self.get_fixtures(path)

    def _get_model_lines(self, name):
        return filter(lambda model: model["model"] == name, self._fixtures)

    def get_model_data(self, name):
        lines = self._get_model_lines(name)
        return list(map(lambda line: line['fields'], lines))


class DB_service:

    def get_model_objects(self, model, data):
        '''возвращает список объектов модели на основе данных'''
        return [model(**line) for line in data]

    def fill_tables(self, models, fixtures):
        '''возвращает список объектов всех моделей на основе fixtures'''
        instances = []
        for model in models:
            data = fixtures.get_model_data(model.__tablename__)
            instances.extend(self.get_model_objects(model, data))
        return instances

    def get_publisher_info(self, **kwargs):
        try:
            publisher = session.query(Publisher).filter_by(**kwargs)
            return publisher.one()
        except NoResultFound:
            return 'No row was found when one was required'


if __name__ == '__main__':

    load_dotenv()
    PG_USER = os.getenv('PG_USER')
    PG_PASSWORD = os.getenv('PG_PASSWORD')
    SERVER = os.getenv('SERVER')
    PORT = os.getenv('PORT')
    DB_NAME = os.getenv('DB_NAME')
    FIXTURES_PATH = 'fixtures/tests_data.json'
    DSN = f'postgresql://{PG_USER}:{PG_PASSWORD}@{SERVER}:{PORT}/{DB_NAME}'

    engine = sq.create_engine(DSN)
    create_tables(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    fixtures = Fixtures(FIXTURES_PATH)
    db = DB_service()

    instances = db.fill_tables((Publisher, Book, Shop, Stock, Sale), fixtures)
    session.add_all(instances)
    session.commit()
    print(db.get_publisher_info(id=1))
    print(db.get_publisher_info(name='Pearson'))

    session.close()
