BOT_NAME = "DiscordBot"
START_COMMAND_PREFIX = "!"
CHANNEL_ID = 817389242874855486
CHANNEL_BOT_ANSWER = 817490081577173052
NOT_FOUND_PREFIX = "Boss not found!"

# COMMAND EXAMPLE !bossName DD.MM.YYYY-HH:MM
COMMAND_LENGTH = 2

JOIN_BOSS_TIMEOUT = 0


AVAILABLE_COMMAND = [
    "help",
    "bossList"
]


# NAME(DON`T CHANGE), <:NAME:ID>
EMOJI_MAP = {
    "emoji_one": "<:Tsundere:818254046934204477>",
    "emoji_two": "<:Nani:818254046669439008>",
    "emoji_three": "<:Care:818254046929616926>",
    "emoji_four": "<:Shy:818254047014420521>",
}

# NAME , ID
MENTION_MAP = {
    "boss1": 817410873882443807,
    "bad":    "Not found :("
}

# NAME, AMOUNT_OF_PEOPLE_TO_GO
BOSSES_MAP = {
    "boss1":  2,
    "bad":    "Not found :("

}
