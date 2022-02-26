from dellus.model import *
from dellus.config import config
from dellus.database.postgresql import PostgreSQLDatabase
from dellus.database.base import Model


class DatabaseFactory:

    @staticmethod
    def create():
        """Get db class from config.db.engine"""
        # TODO: make a utli.mapping
        if config.database['engine'] == 'postgresql':
            database = PostgreSQLDatabase()
        else:
            raise Exception(
                "Unsupported DB type. Supported types are "
                "postgresql")
        database.initialize(config.debug)
        # Create all tables, if not already exists.
        Model.metadata.create_all(database.engine)
        # TODO DB: Run migrations
        return database
