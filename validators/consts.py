from email.policy import default
from enum import Enum


class LoginType(Enum):
    default = "DEFAULT"
    oauth = "OAUTH"
