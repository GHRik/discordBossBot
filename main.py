import asyncio
from datetime import datetime
from time import sleep
import discord

from globals import *
from messageFormater import delete_command_prefix, format_msg, \
    check_user_is_on_list, which_boss_from_mention, get_new_content, split_content,\
    delete_user_from_list, is_special_command, call_special, which_boss_from_content
from mention import make_mention, Mention
from emojiChecker import emoji_counter, is_in_emoji_list
from InfoMessages import error_message, user_exist_message, bad_format_message, create_today_date
from messageValidator import is_validate
from messageHolding import MESSAGES, MESSAGES_TO_CALL, MESSAGES_WAS_CALLED


async def add_emoji_to_msg(message_id):
    for key in EMOJI_MAP:
        await message_id.add_reaction(str(EMOJI_MAP[key]))


async def minion():
    actual_time = create_today_date()
    for mes in MESSAGES:
        split = split_content(mes.content, "\n")
        date = split_content(split[0], "\\s+")
        date = date[1]
        format_date = FORMAT_DATATIME
        msg_date = datetime.strptime(date, format_date)
        sec_to_min = 60.0
        minutes_diff = (msg_date - actual_time).total_seconds() / sec_to_min
        if minutes_diff < INTERVAL_TIME:
            MESSAGES_TO_CALL.append(mes)


class MyClient(discord.Client):

    BOT_REMOVE = False
    BLOCK_ADDING = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("\nConstructor is called:\n")
        self.bg_task = self.loop.create_task(self.spam_emoji_prevent())
        print("Emoji preventer: Online")
        self.bg_task = self.loop.create_task(self.call_after_raid())
        print("Raid checker: Online")
        self.bg_task = self.loop.create_task(self.call_members())
        print("Raid caller: Online")
        self.bg_task = self.loop.create_task(self.fetch_all_message())
        print("Message fetcher : Online")
        self.bg_task = self.loop.create_task(self.purger())
        print("Purger on 00:00 : Online\n\n")
        print("Wait until login... ... ...")

    async def purger(self):
        await self.wait_until_ready()
        while not self.is_closed():
            today = create_today_date()
            if today.hour == 0:
                channel = self.get_channel(CHANNEL_BOT_ANSWER)
                await channel.purge(limit=1000)
                await channel.send("Purge at: "+str(today))
                channel = self.get_channel(CHANNEL_BOT_CALLER)
                await channel.purge(limit=1000)
                await channel.send("Purge at: "+str(today))
            await asyncio.sleep(3600)

    async def fetch_all_message(self):
        fetching_timer = 10
        while not self.is_closed():
            for i in range(len(MESSAGES)):
                message = await client.get_channel(MESSAGES[i].channel.id).fetch_message(MESSAGES[i].id)
                MESSAGES[i] = message
            await asyncio.sleep(fetching_timer)

    async def call_members(self):
        interval = 60
        while not self.is_closed():
            for mes in MESSAGES_TO_CALL:
                if mes in MESSAGES_WAS_CALLED:
                    pass
                else:
                    MESSAGES_WAS_CALLED.append(mes)
                    MESSAGES_TO_CALL.remove(mes)
                    message = await client.get_channel(mes.channel.id).fetch_message(mes.id)
                    mes = message
                    split = split_content(mes.content, "\n")
                    list_of_members = split[1:]
                    temp = ""
                    for elem in list_of_members:
                        temp += elem+"\n"
                    list_of_members = temp
                    date = split_content(split[0], "\\s+")
                    boss = date[0]
                    author = date[3]
                    date = date[1]
                    content = "Guys!\n"+str(list_of_members)+"\n"+str(INTERVAL_TIME)+"min to raid on:\n"+boss
                    content += "\nevent on: "+str(date)+" created by: "+author
                    content += "\n\n!!! Good luck !!!\n\n"
                    channel = self.get_channel(CHANNEL_BOT_CALLER)
                    await channel.send(content)
                    pass
            await asyncio.sleep(interval)

    async def call_after_raid(self):
        checking_timer = 30
        while not self.is_closed():
            await minion()
            await asyncio.sleep(checking_timer)

    async def spam_emoji_prevent(self):
        while not self.is_closed():
            self.BLOCK_ADDING = False
            await asyncio.sleep(JOIN_BOSS_TIMEOUT)

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.channel.id == CHANNEL_BOT_ANSWER:
            if message.content.startswith(START_COMMAND_PREFIX):
                command = delete_command_prefix(message.content)
                if is_special_command(command):
                    context = make_mention(message.author.id, Mention.USER)+"\n"
                    context += call_special(command)
                    channel = self.get_channel(CHANNEL_BOT_ANSWER)
                    await channel.send(context)
                    sleep(0.2)
                elif is_validate(command):
                    split_msg = split_content(command, '\\s+')
                    # Send to channel
                    context = format_msg(split_msg, message.author.id)
                    if context.startswith(NOT_FOUND_PREFIX):
                        channel = self.get_channel(CHANNEL_BOT_ANSWER)
                        await channel.send(context)
                        sleep(0.2)
                    else:
                        channel = self.get_channel(BOSS_CH_ID[which_boss_from_content(message.content)])
                        message_id = await channel.send(context)
                        sleep(0.2)
                        await add_emoji_to_msg(message_id)
                        MESSAGES.append(message_id)
                else:
                    channel = self.get_channel(CHANNEL_BOT_ANSWER)
                    await channel.send(bad_format_message(message.author.id, message.content))
                await message.delete()

    async def on_reaction_add(self, reaction, user):
        if reaction.message.channel.id in BOSS_CH_ID.values():
            if user.name != BOT_NAME:
                if check_user_is_on_list(reaction.message.content, user.id) == -1:
                    if self.BLOCK_ADDING:
                        await reaction.remove(user)
                        author_of_reaction = client.get_channel(CHANNEL_BOT_ANSWER)
                        await author_of_reaction.send("SPAM PREVENTING!!:\n"
                                                      + make_mention(user.id, Mention.USER)
                                                      + "Wait a few second to add")
                        return
                    self.BLOCK_ADDING = True
                    boss = which_boss_from_mention(reaction.message.content)
                    amount_of = int(BOSSES_MAP[boss])
                    if is_in_emoji_list(reaction.emoji):
                        count_of_emoji = emoji_counter(reaction) - len(EMOJI_MAP) + 1
                        if amount_of >= count_of_emoji:
                            await reaction.message.edit(content=get_new_content(user.id, reaction))
                        else:
                            self.BOT_REMOVE = True
                            await reaction.remove(user)
                            author_of_reaction = client.get_channel(CHANNEL_BOT_ANSWER)
                            await author_of_reaction.send(error_message(reaction, user))
                else:
                    self.BOT_REMOVE = True
                    await reaction.remove(user)
                    author_of_reaction = client.get_channel(CHANNEL_BOT_ANSWER)
                    await author_of_reaction.send(user_exist_message(reaction, user))

    async def on_raw_reaction_remove(self, payload):

        channel = self.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        if not self.BOT_REMOVE:
            if check_user_is_on_list(msg.content, payload.user_id) > -1:
                if is_in_emoji_list(str(payload.emoji)):
                    await msg.edit(content=delete_user_from_list(payload, msg.content))
        self.BOT_REMOVE = False

    async def on_raw_message_delete(self, payload):
        if payload.channel_id in BOSS_CH_ID.values():
            for mes in MESSAGES:
                if mes.id == payload.message_id:
                    MESSAGES.remove(mes)
            for mes in MESSAGES_TO_CALL:
                if mes.id == payload.message_id:
                    MESSAGES_TO_CALL.remove(mes)
            for mes in MESSAGES_WAS_CALLED:
                if mes.id == payload.message_id:
                    MESSAGES_WAS_CALLED.remove(mes)


client = MyClient()
client.run('ODE3MzkwMTgyMTM4MzgwMjk4.YEIz7Q.HPHYlrGMts_WS09MtC9OsWU9PmA')
