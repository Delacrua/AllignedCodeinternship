from enum import Enum


class ServerMessage(Enum):
    NICK = 101
    PASS = 102
    REFUSE = 301
    BAN = 401

