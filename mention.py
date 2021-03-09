from enum import Enum
import re


def make_mention(mention_id, option):

    switcher = {
        # <@USER_ID>
        Mention.USER: "<@" + str(mention_id) + ">",
        # <@!USER_ID>
        Mention.USER_NICKNAME: "<@!" + str(mention_id) + ">",
        # <#CHANNEL_ID>
        Mention.CHANNEL: "<#" + str(mention_id) + ">",
        # <@&ROLE_ID>
        Mention.ROLE: "<@&" + str(mention_id) + ">",
    }
    return switcher.get(option)


def decode_mention(mention_id):
    return re.sub('[^A-Za-z0-9]+', '', mention_id)


class Mention(Enum):
    USER = 1
    USER_NICKNAME = 2
    CHANNEL = 3
    ROLE = 4
