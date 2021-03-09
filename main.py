import asyncio
from enum import Enum
from time import sleep
import discord
import re

BOT_NAME = "DiscordBot"
START_COMMAND_PREFIX = "!"
CHANNEL_ID = 817389242874855486
CHANNEL_BOT_ANSWER = 817490081577173052
NOT_FOUND_PREFIX = "Boss not found!"

#COMMAND EXAMPLE !bossName DD.MM.YYYY-HH:MM
COMMAND_LENGTH = 2

JOIN_BOSS_TIMEOUT = 0


#NAME(DONT CHANGE), <:NAME:ID>
EMOJI_MAP = {
    "emoji_one": "<:Tsundere:818254046934204477>",
    "emoji_two": "<:Nani:818254046669439008>",
    "emoji_three": "<:Care:818254046929616926>",
    "emoji_four": "<:Shy:818254047014420521>",
    "NOT_FOUND":    "bad"
}

#NAME , ID
MENTION_MAP = {
    "boss1": 817410873882443807,
    "bad":    "Not found :("
}

#NAME, AMOUNT_OF_PLEOPLE_TO_GO
BOSSES_MAP = {
    "boss1":  2,
    "bad":    "Not found :("

}

def deleteCommandPrexif( command ):
    com = splitContent( command, '\\s+')
    firstWord = com[0]
    firstWordWithoutPrefix = re.sub(START_COMMAND_PREFIX, '', firstWord)
    com[0] = firstWordWithoutPrefix
    myCommand = ""
    for ele in com:
        myCommand += ele+" "
    return myCommand


def splitContent( content, delimRegex ):
    splited = re.split(delimRegex, content)
    while "" in splited:
        del splited[splited.index("")]
    return splited

def createNumberOfMembers( members ):
    numbers = splitContent(members, ',')
    amount = 0
    for elem in numbers:
        amount += int(elem)

    return amount

def makeMention( mentionID, option):

    switcher = {
        Mention.USER: "<@"+str(mentionID)+">",           #<@USER_ID>
        Mention.USER_NICKNAME: "<@!"+str(mentionID)+">", #<@!USER_ID>
        Mention.CHANNEL: "<#"+str(mentionID)+">",        #<#CHANNEL_ID>
        Mention.ROLE: "<@&"+str(mentionID)+">",          #<@&ROLE_ID>
    }
    return switcher.get(option)

def decodeMakeMention( encodedMentionID ):
    return re.sub('[^A-Za-z0-9]+', '', encodedMentionID)


def formatMsg(self, content):
    contex = ""
    if content[0].lower() in MENTION_MAP and content[0].lower() in BOSSES_MAP:
        mention = makeMention(MENTION_MAP[content[0].lower()],Mention.ROLE)
        amoutOfMembers = BOSSES_MAP[content[0].lower()]
        contex += mention
        contex += " "+content[1]

        contex += "\n"
        for i in range(amoutOfMembers):
            contex += ""+str(i+1)+":"+"\n"
        return contex
    else:
        contex = NOT_FOUND_PREFIX+"\nContent:\n"+content[0]+"\n"+"Check bot configuration"
        return contex

def whichBoss( content ):
    bossIdEncoded = content.split(' ', 1)[0]
    bossId = decodeMakeMention(bossIdEncoded)
    for key in MENTION_MAP:
        if MENTION_MAP[key] == int(bossId):
            return key
    return MENTION_MAP["bad"]

def checkUserIsOnList( content, userId ):
    return content.find(str(userId))

def errorMassage( reaction, user ):
    return ("Przekroczona liczba\n" +
     "Na Bossa: " + splitContent(reaction.message.content, " ")[
         0] + "\n"
     + makeMention(user.id,
                   Mention.USER) + " Nie udało Ci się zapisać")
def userExistMessage( content, user ):
    return ("Użytkownik:"+makeMention(user.id,Mention.USER)+"\n"+"Jest już zapisany na: "+splitContent(content.message.content,"\n")[0])

def deleteFirstLineFromContent( content ):
    sansfirstline = '\n'.join(content.split('\n')[1:])
    return sansfirstline

def getFirstFreeSlot( listContent ):
    listOfContent = splitContent(listContent,"\n")
    for i in range(len(listOfContent)):
        listOfContent[i] += "\n"
        regex = r"\d+:(.*)\n"
        result = re.search(regex, listOfContent[i])
        if result.group(1) == "":
            return listOfContent[i][0]
    return -1


def getNewContent(user_id,  reaction):
    mention = makeMention(user_id,Mention.USER)
    myContentWithoutFirstLine = deleteFirstLineFromContent(reaction.message.content)
    freeSlot = getFirstFreeSlot( myContentWithoutFirstLine )
    if freeSlot == -1:
        return reaction.message.content
    else:
        content = splitContent(reaction.message.content, "\n")
        content[int(freeSlot)] = freeSlot+":"+mention+" "+str(reaction.emoji)
        contex = ""
        for i in range(len(content)):
            contex += content[i]+"\n"
        return contex


def deleteUserFromList(payload,  content):
    mention = makeMention(payload.user_id,Mention.USER)
    stringToFind = mention+" "+ str(payload.emoji)
    return content.replace(stringToFind, '')

def isInEmojiList( emoji ):
    for key in EMOJI_MAP:
        if str(emoji) == EMOJI_MAP[key]:
            return True
    return False

def emojiCounter( emojiList ):
    counter = 0
    for i in range(len(emojiList.message.reactions)):
        counter += emojiList.message.reactions[i].count
    return counter

class Mention(Enum):
    USER = 1
    USER_NICKNAME = 2
    CHANNEL = 3
    ROLE = 4


class MyClient(discord.Client):

    BOT_REMOVE = False
    BLOCK_ADDING = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bg_task = self.loop.create_task(self.spamEmojiPrevent())

    async def spamEmojiPrevent(self):
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
                command = deleteCommandPrexif(message.content)
                splitedMsg = splitContent(command,'\\s+')
                if len(splitedMsg) == COMMAND_LENGTH:

                    #Send to channel
                    contex = formatMsg(self, splitedMsg)
                    if contex.startswith(NOT_FOUND_PREFIX):
                        channel = self.get_channel(CHANNEL_BOT_ANSWER)
                        await channel.send(contex)
                        sleep(0.2)
                    else:
                        channel = self.get_channel(CHANNEL_ID)
                        id = await channel.send(contex)
                        sleep(0.2)
                        await id.add_reaction(EMOJI_MAP["emoji_one"])
                        await id.add_reaction(EMOJI_MAP["emoji_two"])
                        await id.add_reaction(EMOJI_MAP["emoji_three"])
                        await id.add_reaction(EMOJI_MAP["emoji_four"])
                else:
                    channel = self.get_channel(CHANNEL_BOT_ANSWER)
                    await channel.send("Bad message:\nFormat should be: !bossName DD:MM:YYYY-HH:MM\nYour format: "+message.content)
                await message.delete()

    async def on_reaction_add(self, reaction, user):
        if reaction.message.channel.id == CHANNEL_ID:
            if user.name != BOT_NAME:
                if checkUserIsOnList(reaction.message.content, user.id) == -1:
                    if self.BLOCK_ADDING == True:
                        await reaction.remove(user)
                        authorOfReaction = client.get_channel(CHANNEL_BOT_ANSWER)
                        await authorOfReaction.send("SPAM PREVENTING!!:\n"+makeMention(user.id,Mention.USER)+ "Wait a few second to add")
                        return
                    self.BLOCK_ADDING = True
                    boss = whichBoss(reaction.message.content)
                    amountOF = int(BOSSES_MAP[boss])
                    if isInEmojiList(reaction.emoji) == True:
                        countOfEmoji = emojiCounter(reaction)-len(EMOJI_MAP)+1
                        if( amountOF >= countOfEmoji ):
                            await reaction.message.edit(content= getNewContent(user.id, reaction))
                        else:
                            self.BOT_REMOVE = True
                            await reaction.remove(user)
                            authorOfReaction = client.get_channel(CHANNEL_BOT_ANSWER)
                            await authorOfReaction.send( errorMassage( reaction ,user ) )
                else:
                    self.BOT_REMOVE = True
                    await reaction.remove(user)
                    authorOfReaction = client.get_channel(CHANNEL_BOT_ANSWER)
                    await authorOfReaction.send(userExistMessage( reaction,user ))



    async def on_raw_reaction_remove(self, payload):

        await self.wait_until_ready()
        channel = self.get_channel(CHANNEL_ID)
        msg = await channel.fetch_message(payload.message_id)
        if self.BOT_REMOVE == False:
            if  checkUserIsOnList(msg.content, payload.user_id) > -1 :
                if str(payload.emoji) == EMOJI_MAP["emoji_one"]:
                    await msg.edit(content= deleteUserFromList(payload, msg.content))
                    sleep(0.2)
                if str(payload.emoji) == EMOJI_MAP["emoji_two"]:
                    await msg.edit(content= deleteUserFromList(payload, msg.content))
                if str(payload.emoji) == EMOJI_MAP["emoji_three"]:
                    await msg.edit(content= deleteUserFromList(payload, msg.content))
                    sleep(0.2)
                if str(payload.emoji) == EMOJI_MAP["emoji_four"]:
                    await msg.edit(content= deleteUserFromList(payload, msg.content))
                    sleep(0.2)
        self.BOT_REMOVE = False



client = MyClient()
client.run('ODE3MzkwMTgyMTM4MzgwMjk4.YEIz7Q.HPHYlrGMts_WS09MtC9OsWU9PmA')
