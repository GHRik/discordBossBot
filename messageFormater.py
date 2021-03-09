import re
from globals import START_COMMAND_PREFIX, BOSSES_MAP, MENTION_MAP, NOT_FOUND_PREFIX
from mention import make_mention, decode_mention, Mention


def format_msg(content):
    context = ""
    if content[0].lower() in MENTION_MAP and content[0].lower() in BOSSES_MAP:
        mention = make_mention(MENTION_MAP[content[0].lower()], Mention.ROLE)
        amount_of_members = BOSSES_MAP[content[0].lower()]
        context += mention
        context += " "+content[1]

        context += "\n"
        for i in range(amount_of_members):
            context += ""+str(i+1)+":"+"\n"
        return context
    else:
        context = NOT_FOUND_PREFIX+"\nContent:\n"+content[0]+"\n"+"Check bot configuration"
        return context


def delete_first_line(content):
    sans_first_line = '\n'.join(content.split('\n')[1:])
    return sans_first_line


def get_new_content(user_id, reaction):
    mention = make_mention(user_id, Mention.USER)
    content_without_first_line = delete_first_line(reaction.message.content)
    free_slot = get_first_free_slot(content_without_first_line)
    if free_slot == -1:
        return reaction.message.content
    else:
        content = split_content(reaction.message.content, "\n")
        content[int(free_slot)] = free_slot+":"+mention+" "+str(reaction.emoji)
        context = ""
        for i in range(len(content)):
            context += content[i]+"\n"
        return context


def which_boss(content):
    boss_id_encoded = content.split(' ', 1)[0]
    boss_id = decode_mention(boss_id_encoded)
    for key in MENTION_MAP:
        if MENTION_MAP[key] == int(boss_id):
            return key
    return MENTION_MAP["bad"]


def check_user_is_on_list(content, user_id):
    return content.find(str(user_id))


def get_first_free_slot(list_content):
    list_of_content = split_content(list_content, "\n")
    for i in range(len(list_of_content)):
        list_of_content[i] += "\n"
        regex = r"\d+:(.*)\n"
        result = re.search(regex, list_of_content[i])
        if result.group(1) == "":
            return list_of_content[i][0]
    return -1


def delete_user_from_list(payload, content):
    mention = make_mention(payload.user_id, Mention.USER)
    string_to_find = mention+" " + str(payload.emoji)
    return content.replace(string_to_find, '')


def delete_command_prefix(command):
    com = split_content(command, '\\s+')
    first_word = com[0]
    first_word_without_prefix = re.sub(START_COMMAND_PREFIX, '', first_word)
    com[0] = first_word_without_prefix
    my_command = ""
    for ele in com:
        my_command += ele+" "
    return my_command


def split_content(content, delimiter_regex):
    split = re.split(delimiter_regex, content)
    while "" in split:
        del split[split.index("")]
    return split


def create_number_of_members(members):
    numbers = split_content(members, ',')
    amount = 0
    for elem in numbers:
        amount += int(elem)

    return amount
