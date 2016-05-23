import threading


class PollHelper:
    def __init__(self, interface_layer):
        self._interface_layer = interface_layer
        self._is_poll = False
        self._question = None
        self._poll_options = []
        self._votes = {}
        self._voters = {}
        self._chat_id = -1

    def start_poll(self, chat_id, question, options):
        if self._is_poll:
            raise AlreadyPollingException
        if len(options) == 0 or question == '':
            raise InvalidVoteException

        self._is_poll = True
        self._question = question
        self._poll_options += options
        self._chat_id = chat_id
        for i in range(1, len(options) + 1):
            self._votes[i] = 0

        # t = threading.Timer(30, self.timer_end_poll)
        # t.start()

    def vote(self, option, from_id):
        if option < 1 or option > len(self._poll_options):
            raise InvalidVoteException
        if self._voters.get(from_id):
            raise AlreadyVotedException
        self._votes[option] += 1
        self._voters[from_id] = True

    def end_poll(self):
        if not self._is_poll:
            raise NoPollActive
        max_vote = max(self._votes, key=self._votes.get)
        winner = self._poll_options[max_vote - 1]
        num_votes = max(self._votes.values())

        results = []
        for i in range(1, len(self._poll_options) + 1):
            results.append((self._votes[i], self._poll_options[i - 1]))


        self._is_poll = False
        self._question = None
        self._votes = {}
        self._poll_options = []
        self._voters = {}

        return winner, num_votes, results

    def get_question(self):
        return self._question

    def get_options(self):
        return self._poll_options

    # def timer_end_poll(self):
    #     question = self._question
    #     try:
    #         winner = self.end_poll()
    #         self._router.timer_end_poll(self._chat_id, question, winner)
    #     except:
    #         pass # poll already ended


class AlreadyPollingException(Exception):
    pass


class InvalidVoteException(Exception):
    pass


class AlreadyVotedException(Exception):
    pass


class NoPollActive(Exception):
    pass
