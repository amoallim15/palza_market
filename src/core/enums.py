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
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class BannerLocation(str, enum.Enum):
    BANNER_01 = "BANNER_01"
    BANNER_02 = "BANNER_02"
    BANNER_03 = "BANNER_03"
    BANNER_04 = "BANNER_04"
    BANNER_05 = "BANNER_05"
    BANNER_06 = "BANNER_06"
    BANNER_07 = "BANNER_07"
    BANNER_08 = "BANNER_08"
    BANNER_09 = "BANNER_09"
    BANNER_10 = "BANNER_10"
    BANNER_11 = "BANNER_11"
    BANNER_12 = "BANNER_12"


class ReviewType(str, enum.Enum):
    PURCHASE = "PURCHASE"
    SALE = "SALE"
