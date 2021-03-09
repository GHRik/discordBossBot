from mention import Mention, make_mention
from messageFormater import split_content


def error_message(reaction, user):
    return ("Przekroczona liczba\n" +
            "Na Bossa: " + split_content(reaction.message.content, " ")[0]
            + "\n"
            + make_mention(user.id,
                           Mention.USER) + " Nie udało Ci się zapisać")


def user_exist_message(content, user):
    return "Użytkownik:" + make_mention(user.id, Mention.USER) + "\n" + "Jest już zapisany na: " \
           + split_content(content.message.content, "\n")[0]
