from globals import EMOJI_MAP


def is_in_emoji_list(emoji):
    for key in EMOJI_MAP:
        if str(emoji) == EMOJI_MAP[key]:
            return True
    return False


def emoji_counter(emoji_list):
    counter = 0
    for i in range(len(emoji_list.message.reactions)):
        counter += emoji_list.message.reactions[i].count
    return counter
