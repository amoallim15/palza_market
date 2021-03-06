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
    async def connect(self):
        raise NotImplementedError

    @abstractmethod
    async def close(self):
        raise NotImplementedError


class MongoStore(BaseDataStore):

    FIELDS = ["host", "port", "username", "password", "database", "protocol"]

    async def connect(self):
        url = f"{self.protocol}://{self.username}:{self.password}@{self.host}/{self.database}?retryWrites=true&w=majority"
        self.connector = connector = motor.motor_asyncio.AsyncIOMotorClient(url)
        return getattr(connector, self.database)

    async def close(self):
        self.connector.close()
        pass


class ObjectStore(BaseDataStore):

    FIELDS = ["aws_access_key_id", "aws_secret_access_key", "aws_region"]

    async def connect(self):
        self.connector = connector = boto3.resource(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region,
        )
        return connector

    async def close(self):
        pass
