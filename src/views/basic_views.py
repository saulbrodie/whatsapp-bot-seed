from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from random import randint
from utils.countdown import get_countdown
from utils.PollHelper import *
from views.media import MediaViews

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

def overwatch_hype(message, match, router):
    media_views = MediaViews(router)
    media_views.image_sender.send_by_url(jid=message.getFrom(), file_url='http://assets.vg247.com/current/2015/09/overwatch.jpg')
    router.toLower(TextMessageProtocolEntity('OVERWATCH HYPEEE!', to=message.getFrom()))

def start_poll(message, match, router):
    question = match.group('question')
    options = match.group('options').split(' ')

    try:
        router._poll_helper.start_poll(message.getFrom(), question, options)
        router.toLower(TextMessageProtocolEntity(question + '?', to=message.getFrom()))
        for i in range(1, len(options) + 1):
            router.toLower(TextMessageProtocolEntity(str(i) + ': ' + options[i - 1], to=message.getFrom()))
    except AlreadyPollingException:
        router.toLower(TextMessageProtocolEntity('Please finish your poll first', to=message.getFrom()))
    except:
        router.toLower(TextMessageProtocolEntity('Invalid arguments for poll', to=message.getFrom()))


def vote(message, match, router):
    try:
        num = match.group('number')
        num = int(num, 10)
        router._poll_helper.vote(num, message.getAuthor())
        router.toLower(TextMessageProtocolEntity('Thank you for your vote!', to=message.getFrom()))
    except InvalidVoteException:
        router.toLower(TextMessageProtocolEntity('Invalid vote', to=message.getFrom()))
    except AlreadyVotedException:
        router.toLower(TextMessageProtocolEntity('Already voted', to=message.getFrom()))
    except:
        router.toLower(TextMessageProtocolEntity('Invalid choice', to=message.getFrom()))


def end_poll(message, match, router):
    try:
        question = router._poll_helper.get_question()
        winner, num_votes, results = router._poll_helper.end_poll()

        RESULTS = ''
        for element in results:
            RESULTS += element[1] + ' with ' + str(element[0]) + ' votes.\n'

        router.toLower(TextMessageProtocolEntity(
            u'\U0001f4ca' + 'Poll ended! here are the results:\n' + question + '?\n' + 'Winner is: ' + winner +
            ' with ' + str(num_votes) + ' votes!', to=message.getFrom()))

        router.toLower(TextMessageProtocolEntity(RESULTS, to=message.getFrom()))
    except NoPollActive:
        router.toLower(TextMessageProtocolEntity('No poll active, end what?', to=message.getFrom()))
