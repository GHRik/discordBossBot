from datetime import datetime

from mention import Mention, make_mention
import re


def error_message(reaction, user):
    return ("Przekroczona liczba\n" +
            "Na Bossa: " + split_content(reaction.message.content, " ")[0]
            + "\n"
            + make_mention(user.id,
                           Mention.USER) + " Nie udało Ci się zapisać")


def user_exist_message(content, user):
    return "Użytkownik:" + make_mention(user.id, Mention.USER) + "\n" + "Jest już zapisany na: " \
           + split_content(content.message.content, "\n")[0]


def bad_format_message(user_id, content):
    today = create_today_date()
    return str(make_mention(user_id, Mention.USER)+" Input bad format:\n"
               "```Format should be: !COMMAND DD:MM:YYYY-HH:MM > "+str(today)+"```\n```Your format: " + content+"```")


def print_help(command_dict):
    output = "Bot created by RiK\n\n"
    output += "This is helper bot to create raid event on bosses.\n"
    output += "If you want to create raid call:"
    output += "```!bossName DD:MM:YYYY-HH:MM ```"
    output += "After that, you can easy enjoy event by clicking one of emoji under created post\n"
    output += "if you change your mind you can easy remove you from event by clicking your active emoji.\n"
    output += "\nCommands available: "
    output += "```\n"
    for key in command_dict:
        output += key+"\n"
    output += "```"
    output += "Under help you will se available bosses to raid... " \
              "\nIn the future for list you can call: \n```!bossList```\n"
    output += "If you saw any bug, report me or admin of this server ;)\n"
    return output


def print_boss_list(bosses_dict):
    output = "\nBoss available: \n"
    output += "```"
    for key in bosses_dict:
        if key != "bad":
            output += "!"+key+"\n"
    output += "```"
    return output


def split_content(content, delimiter_regex):
    split = re.split(delimiter_regex, content)
    while "" in split:
        del split[split.index("")]
    return split


def create_today_date():
    today = datetime.today().date()
    today_hours = datetime.today().time()
    today_hours = str(today_hours.hour) + ":" + str(today_hours.minute)
    today_date = str(today.day) + "." + str(today.month) + "." + str(today.year)
    today_date = today_date + "-" + today_hours
    format_date = "%d.%m.%Y-%H:%M"
    today = datetime.strptime(today_date, format_date)
    return today
