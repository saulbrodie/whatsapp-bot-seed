from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from random import randint

BOT_SAUL_DICT = ('fangay', 'apple sucks', 'overwatch arcade game', 'hearthstone pooping game',
                 'game of thrones is overrated', 'blizzard is bad')

def echo(message, match):
    return TextMessageProtocolEntity("%s" % match.group("echo_message"), to=message.getFrom())

def trihard(message, match):
    return TextMessageProtocolEntity(BOT_SAUL_DICT[randint(0, len(BOT_SAUL_DICT) - 1)], to=message.getFrom())