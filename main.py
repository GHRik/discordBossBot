import asyncio
from time import sleep
import discord

from globals import *
from messageFormater import delete_command_prefix, format_msg, \
    check_user_is_on_list, which_boss, get_new_content, split_content,\
    delete_user_from_list, is_special_command, call_special
from mention import make_mention, Mention
from emojiChecker import emoji_counter, is_in_emoji_list
from InfoMessages import error_message, user_exist_message, bad_format_message
from messageValidator import is_validate


async def add_emoji_to_msg(message_id):
    for key in EMOJI_MAP:
        await message_id.add_reaction(str(EMOJI_MAP[key]))


class MyClient(discord.Client):

    BOT_REMOVE = False
    BLOCK_ADDING = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_task = self.loop.create_task(self.spam_emoji_prevent())

    async def spam_emoji_prevent(self):
        await self.wait_until_ready()
        while not self.is_closed():
            self.BLOCK_ADDING = False
            await asyncio.sleep(JOIN_BOSS_TIMEOUT)

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        await self.wait_until_ready()
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.channel.id == CHANNEL_ID:
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
                        channel = self.get_channel(CHANNEL_ID)
                        message_id = await channel.send(context)
                        sleep(0.2)
                        await add_emoji_to_msg(message_id)
                else:
                    channel = self.get_channel(CHANNEL_BOT_ANSWER)
                    await channel.send(bad_format_message(message.author.id, message.content))
                await message.delete()

    async def on_reaction_add(self, reaction, user):
        if reaction.message.channel.id == CHANNEL_ID:
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
                    boss = which_boss(reaction.message.content)
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

        channel = self.get_channel(CHANNEL_ID)
        msg = await channel.fetch_message(payload.message_id)
        if not self.BOT_REMOVE:
            if check_user_is_on_list(msg.content, payload.user_id) > -1:
                if is_in_emoji_list(str(payload.emoji)):
                    await msg.edit(content=delete_user_from_list(payload, msg.content))
        self.BOT_REMOVE = False


client = MyClient()
client.run('ODE3MzkwMTgyMTM4MzgwMjk4.YEIz7Q.HPHYlrGMts_WS09MtC9OsWU9PmA')
