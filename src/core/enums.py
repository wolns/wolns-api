from enum import StrEnum, auto


class PositionEnum(StrEnum):
    UP = auto()
    STAY = auto()
    DOWN = auto()


class PlatformEnum(StrEnum):
    YANDEX = auto()
    SPOTIFY = auto()


class FollowStatusEnum(StrEnum):
    SUBSCRIBER = auto()
    SUBSCRIBED = auto()
    FRIEND = auto()
