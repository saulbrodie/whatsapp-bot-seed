from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from utils.PollHelper import *


# Basic regex routes
class PollViews():
    def __init__(self, basic_views):
        self.basic_views = basic_views
        self._poll_helper = PollHelper(self)

    def generate_poll_message(self):
        question = self._poll_helper.get_question()
        options = self._poll_helper.get_options()
        MESSAGE = str(question) + '?\n'

        for i in range(1, len(options) + 1):
            MESSAGE += str(i) + ': ' + options[i - 1] + '\n'

        return MESSAGE

    def start_poll(self, message, match):
        question = match.group('question')
        options = match.group('options').split(' ')

        try:
            self._poll_helper.start_poll(message.getFrom(), question, options)
            MESSAGE = self.generate_poll_message()
            self.basic_views.send_text(MESSAGE, message.getFrom())

        except AlreadyPollingException:
            MESSAGE = self.generate_poll_message()
            self.basic_views.send_text('Please finish your poll first\n' + MESSAGE, message.getFrom())
        except:
            self.basic_views.send_text('Invalid arguments for poll', message.getFrom())

    def vote(self, message, match):
        try:
            num = match.group('number')
            num = int(num, 10)
            self._poll_helper.vote(num, message.getAuthor())
            self.basic_views.send_text('Thank you for your vote!', message.getFrom())
        except InvalidVoteException:
            self.basic_views.send_text('Invalid vote', message.getFrom())
        except AlreadyVotedException:
            self.basic_views.send_text('Already voted', message.getFrom())
        except:
            self.basic_views.send_text('Invalid choice', message.getFrom())

    def end_poll(self, message, match):
        try:
            question = self._poll_helper.get_question()
            winner, num_votes, results = self._poll_helper.end_poll()

            RESULTS = ''
            for element in results:
                RESULTS += element[1] + ': ' + str(element[0]) + ' votes.\n'

            self.basic_views.send_text(
                u'\U0001f4ca' + 'Poll ended! here are the results:\n' + question + '?\n' + 'Winner is: ' + winner +
                ' with ' + str(num_votes) + ' votes!', message.getFrom())

            self.basic_views.send_text(RESULTS, message.getFrom())
        except NoPollActive:
            self.basic_views.send_text('No poll active, end what?', message.getFrom())
