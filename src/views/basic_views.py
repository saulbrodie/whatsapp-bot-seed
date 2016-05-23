from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from random import randint
from utils.countdown import get_countdown

BOT_SAUL_DICT = ('fangay', 'apple sucks', 'overwatch arcade game', 'hearthstone pooping game',
                 'game of thrones is overrated', 'blizzard is bad')

def echo(message, match, router):
    return TextMessageProtocolEntity("%s" % match.group("echo_message"), to=message.getFrom())

def trihard(message, match, router):
    trihard_emojis = u'\U0001f575'
    trihard_emojis *= 3
    MESSAGE = BOT_SAUL_DICT[randint(0, len(BOT_SAUL_DICT) - 1)] + trihard_emojis
    return TextMessageProtocolEntity(MESSAGE, to=message.getFrom())

def overwatch_countdown(message, match, router):
    MESSAGE = '''OVERWATCH BEGINS IN: %s.
                 DON\'T BE LATE!''' % get_countdown(2016, 05, 24, 02)
    return TextMessageProtocolEntity("%s" % MESSAGE, to=message.getFrom())

def start_poll(message, match, router):
    question = match.group('question')
    options = match.group('options').split(' ')

    try:
        router._poll_helper.start_poll(message.getFrom(), question, options)
        router.toLower(TextMessageProtocolEntity('got it: %s' % question, to=message.getFrom()))
    except:
        pass
