import enum


class UserType(str, enum.Enum):
    AGENCY = "AGENCY"
    INDIVIDUAL = "INDIVIDUAL"


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    EMPLOYEE = "EMPLOYEE"
    CLIENT = "CLIENT"


class UserMethod(str, enum.Enum):
    EMAIL = "EMAIL"
    KAKAO = "KAKAO"
    NAVER = "NAVER"
    GOOGLE = "GOOGLE"


class CrontabStatus(str, enum.Enum):
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
