from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from random import randint
from utils.countdown import get_countdown
from utils.PollHelper import *
from views.media import MediaViews

BOT_SAUL_DICT = ('fangay', 'apple sucks', 'overwatch arcade game', 'hearthstone pooping game',
                 'game of thrones is overrated', 'blizzard is bad')


# Basic regex routes
class BasicViews():
    def __init__(self, interface_layer):
        self.interface_layer = interface_layer
        self.media_views = MediaViews(interface_layer)

        self.routes = [
            ("^/e(cho)?\s(?P<echo_message>[^$]+)$", self.echo),
            ('^/trihard$', self.trihard),
            ('^/countdown$', self.overwatch_countdown),
            ('^/poll\s(?P<question>.+)\?\s(?P<options>.*)$', self.start_poll),
            ('^/vote\s(?P<number>\d)$', self.vote),
            ('^/endpoll$', self.end_poll),
            ('.*(overwatch)|(OVERWATCH)|(Overwatch).*$', self.overwatch_hype),
        ]

    def send_text(self, data, to):
        self.interface_layer.toLower(TextMessageProtocolEntity(data, to=to))

    def send_image(self, url, to):
        self.media_views.image_sender.send_by_url(jid=to, file_url=url)

    def echo(self, message, match):
        self.send_text(match.group("echo_message"), message.getFrom())

    def trihard(self, message, match):
        trihard_emojis = u'\U0001f575'
        trihard_emojis *= 3
        MESSAGE = BOT_SAUL_DICT[randint(0, len(BOT_SAUL_DICT) - 1)] + ' ' + trihard_emojis
        self.send_image('http://orig09.deviantart.net/5253/f/2012/084/3/3/pewdiepie__try_hard_face_by_arashidaisuki-d4tw9js.png', message.getFrom())
        self.send_text(MESSAGE, message.getFrom())

    def overwatch_countdown(self, message, match):
        MESSAGE = '''OVERWATCH BEGINS IN: %s.
                     DON\'T BE LATE!''' % get_countdown(2016, 05, 24, 02)
        self.send_text(MESSAGE, message.getFrom())

    def overwatch_hype(self, message, match):
        self.send_image('http://assets.vg247.com/current/2015/09/overwatch.jpg', message.getFrom())
        self.send_text('OVERWATCH HYPEEE!', message.getFrom())

    def start_poll(self, message, match):
        question = match.group('question')
        options = match.group('options').split(' ')

        try:
            router._poll_helper.start_poll(message.getFrom(), question, options)
            self.send_text(question + '?', message.getFrom())
            for i in range(1, len(options) + 1):
                self.send_text(str(i) + ': ' + options[i - 1], message.getFrom())
        except AlreadyPollingException:
            self.send_text('Please finish your poll first', message.getFrom())
        except:
            self.send_text('Invalid arguments for poll', message.getFrom())

    def vote(self, message, match):
        try:
            num = match.group('number')
            num = int(num, 10)
            router._poll_helper.vote(num, message.getAuthor())
            self.send_text('Thank you for your vote!', message.getFrom())
        except InvalidVoteException:
            self.send_text('Invalid vote', message.getFrom())
        except AlreadyVotedException:
            self.send_text('Already voted', message.getFrom())
        except:
            self.send_text('Invalid choice', message.getFrom())

    def end_poll(self, message, match):
        try:
            question = router._poll_helper.get_question()
            winner, num_votes, results = router._poll_helper.end_poll()

            RESULTS = ''
            for element in results:
                RESULTS += element[1] + ' with ' + str(element[0]) + ' votes.\n'

            self.send_text(
                u'\U0001f4ca' + 'Poll ended! here are the results:\n' + question + '?\n' + 'Winner is: ' + winner +
                ' with ' + str(num_votes) + ' votes!', message.getFrom())

            self.send_text(RESULTS, message.getFrom())
        except NoPollActive:
            self.send_text('No poll active, end what?', message.getFrom())
