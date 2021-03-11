from datetime import datetime

from globals import FORMAT_DATATIME
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
               "```Format should be: !COMMAND DD:MM:YYYY-HH:MM > "+str(today)+"```\n```Your format: " + content + "```"
               + "\n\nCall: ```!help``` for more info\n")


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


def print_today_list(message_list):
    today = []
    today_date = create_today_date()

    for mes in message_list:
        split = split_content(mes.content, "\n")
        split = split_content(split[0], "\\s+")
        date = split[1]
        format_date = FORMAT_DATATIME
        date = datetime.strptime(date, format_date)
        if date.date() == today_date.date():
            today.append(mes)
    result = "TODAY EVENTS: \n"
    counter = 0
    today_list = sort_message_by_date(today)
    for mes in today_list:
        counter += 1
        split = split_content(mes.content, "\n")
        result += str(counter) + ". Event " + ": " + split[0] + "\n"
        split = split_content(split[0], "\\s+")
        date = split[1]
        format_date = FORMAT_DATATIME
        date = datetime.strptime(date, format_date)
        sec_to_min = 60.0
        minutes_diff = (date - today_date).total_seconds() / sec_to_min
        if minutes_diff > 0:
            result += "To go: " + str(minutes_diff) + " min"
        else:
            result += "Was started: " + str(minutes_diff) + "min ago"
        list_members = []
        split = split_content(mes.content, "\n")
        split = split[1:]
        for member in split:
            list_members.append(member)
        result += "\t\tFree slots: " + get_slots(list_members) + "\n"
    if len(today) == 0:
        result += "No event today\n\n For list all event: ```!eventList```"
    return result


def print_active_list(message_list):
    event = []
    today_date = create_today_date()
    for mes in message_list:
        split = split_content(mes.content, "\n")
        split = split_content(split[0], "\\s+")
        date = split[1]
        format_date = FORMAT_DATATIME
        date = datetime.strptime(date, format_date)
        if date.date() >= today_date.date():
            event.append(mes)
    result = "ACTIVE EVENTS: \n"
    counter = 0
    event = sort_message_by_date(event)
    for mes in event:
        counter += 1
        split = split_content(mes.content, "\n")
        result += str(counter) + ". Event " + ": " + split[0] + "\n"
        list_members = []
        split = split_content(mes.content, "\n")
        split = split[1:]
        for member in split:
            list_members.append(member)
        result += "\t\tFree slots: " + get_slots(list_members) + "\n"
    if len(event) == 0:
        result += "No active event\n\n If you want to know how to create event: ```!help```"
    return result


def print_user_active_event(user_id, message_list):
    event = []
    today_date = create_today_date()
    for mes in message_list:
        split = split_content(mes.content, "\n")
        members = ""
        for member in split[1:]:
            members += member
        split = split_content(split[0], "\\s+")
        date = split[1]
        format_date = FORMAT_DATATIME
        date = datetime.strptime(date, format_date)
        if date.date() >= today_date.date() and members.count(str(user_id)) > 0:
            event.append(mes)
    result = "ONLY YOURS ACTIVE EVENTS: \n"
    counter = 0
    event = sort_message_by_date(event)
    for mes in event:
        counter += 1
        split = split_content(mes.content, "\n")
        result += str(counter) + ". Event " + ": " + split[0] + "\n"
    if len(event) == 0:
        result += "No active event\n\n If you want to know how to create event: ```!help```"
    return result


def sort_message_by_date(message_list):
    temp_dict = {}
    for mes in message_list:
        split = split_content(mes.content, "\n")
        split = split_content(split[0], "\\s+")
        date = split[1]
        format_date = FORMAT_DATATIME
        date = datetime.strptime(date, format_date)
        temp_dict[mes] = date

    temp_dict = sorted(temp_dict, key=temp_dict.get)
    message_list.clear()
    for mes in temp_dict:
        message_list.append(mes)
    return message_list


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
    format_date = FORMAT_DATATIME
    today = datetime.strptime(today_date, format_date)
    return today


def get_slots(list_content):
    maksimum = len(list_content)
    free = 0
    for i in range(len(list_content)):
        list_content[i] += "\n"
        regex = r"\d+:(.*)\n"
        result = re.search(regex, list_content[i])
        if result.group(1) == "":
            free += 1
    return str(free)+"/"+str(maksimum)
