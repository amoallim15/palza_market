import boto3
from abc import ABC, abstractmethod
from pymongo import MongoClient


class BaseDataStore(ABC):

    FIELDS = []

    def __init__(self, **kwargs):
        self.connection = {}
        for field in self.FIELDS:
            if field not in kwargs:
                raise ValueError(
                    f"connection string is malformed, missing {field} field."
                )
            setattr(self, field, kwargs[field])

    @abstractmethod
    def connect(self):
        raise NotImplementedError


class MongoStore(BaseDataStore):

    FIELDS = ["host", "port", "user", "pwd", "db"]

    def connect(self):
        connector = MongoClient(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.pwd,
            retryWrites=False,
        )
        return getattr(connector, "db")
