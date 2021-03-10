
# NAME OF YOUR DISCORD BOT
BOT_NAME = "DiscordBot"
# PREFIX TO START COMMAND FOR EXAMPLE !help , if you change this, for example on: "bossHelper!" command willbe look
# like bosshelper!help
START_COMMAND_PREFIX = "!"

# CHANNEL WHICH ALL COMMENDS ALL CALL FOR EXAMPLE HELP,BOSSLIST ETC.
CHANNEL_ID = 817389242874855486

# CHANNEL WHICH BOT ANSWER TO YOU, IN ANY CASE OF BAD INPUT OR PROBLEM WITH JOIN ON RAID
CHANNEL_BOT_ANSWER = 817490081577173052

# CHANNEL WHICH BOT CALL INTERVAL_TIME AFTER RAID
CHANNEL_BOT_CALLER = 818890497153957968

# TIME IN MINUTES TO CALL A PEOPLE WHICH GOING ON RAID
INTERVAL_TIME = 30

JOIN_BOSS_TIMEOUT = 0

# SPECIAL COMMAND TO USE
AVAILABLE_COMMAND = [
    "help",
    "bossList",
    "today",
    "eventList"
]

# YOUR CUSTOM EMOJI
# NAME(DON`T CHANGE), <:NAME:ID>
EMOJI_MAP = {
    "emoji_one": "<:Tsundere:818254046934204477>",
    "emoji_two": "<:Nani:818254046669439008>",
    "emoji_three": "<:Care:818254046929616926>",
    "emoji_four": "<:Shy:818254047014420521>",
}

# MENTION A BOSS ROLE, NAME SHOULD BE SAME AS ROLE ON SERVER.
# NAME , ID
MENTION_MAP = {
    "boss1": 817410873882443807,
    "bad":    "Not found :("
}

# NAME SHOULD BE SAME AS ROLE ON SERVER.
# NAME, AMOUNT_OF_PEOPLE_TO_GO
BOSSES_MAP = {
    "boss1":  99,
    "bad":    "Not found :("

}

# !!!!!  DONT CHANGE ZONE   !!!!
# ----------------------------------------------------------------------------------------------------------------------

# COMMAND EXAMPLE !bossName DD.MM.YYYY-HH:MM
COMMAND_LENGTH = 2
FORMAT_DATE = "%d.%m.%Y"
FORMAT_TIME = "%H:%M"
FORMAT_DATATIME = "%d.%m.%Y-%H:%M"
NOT_FOUND_PREFIX = "Boss not found!"
