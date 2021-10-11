import enum


class UserType(enum.Enum):
    AGENCY = 1
    INDIVIDUAL = 2


class UserRole(enum.Enum):
    ADMIN = 1
    EMPLOYEE = 2
    NORMAL = 3


class UserMethod(enum.Enum):
    EMAIL = 1
    KAKAO = 2
    NAVER = 3
    GOOGLE = 4


class CrontabStatus(enum.Enum):
    RUNNING = 1
    SUCCEEDED = 2
    FAILED = 3
