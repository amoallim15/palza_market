from abc import ABC, abstractmethod
import boto3
import motor.motor_asyncio


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

    FIELDS = ["host", "port", "username", "password", "database"]

    def connect(self):
        url = f"mongodb://{self.username}:{self.password}@{self.host}/{self.database}?retryWrites=false&replicaSet=rs0&readPreference=secondaryPreferred"
        connector = motor.motor_asyncio.AsyncIOMotorClient(url)
        return getattr(connector, self.database)


class ObjectStore(BaseDataStore):

    FIELDS = ["aws_access_key_id", "aws_secret_access_key", "aws_region"]

    def connect(self):
        connector = boto3.resource(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region,
        )
        return connector
