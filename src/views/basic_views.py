from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from random import randint
from utils.countdown import get_countdown
from utils.PollHelper import *
from utils.media_sender import *
from views.media import MediaViews
from views.poll_views import PollViews

BOT_SAUL_DICT = ('Fangay', 'Apple sucks', 'Overwatch good arcade game', 'Hearthstone pooping game',
                 'Game of thrones is overrated', 'SDYF' ,'SDAA')

NIGGRO_MODE = ('Bring dem fuckin rockets to dat ass', 'Bend that bitch like beckham', 'I dont fuck around',
               'Im de president of hittin dat ass', 'Never hand a dick to someone with parkinsons', 
               'Imma fuck you ass up')
               
SUKDIK = ('YuvalFatael', 'AdamSwid', 'SaulBrodie', 'AmitAlfassy', 'GalPressman', 'OrDicker')


# Basic regex routes
class BasicViews():
    def __init__(self, interface_layer):
        self.interface_layer = interface_layer
        self.image_sender = ImageSender(interface_layer)
        self.video_sender = VideoSender(interface_layer)
        self.audio_sender = AudioSender(interface_layer)
        self.media_views = MediaViews(interface_layer)
        self.poll_views = PollViews(self)

        self.routes = [
            ("^/e(cho)?\s(?P<echo_message>[^$]+)$", self.echo),
            ('^/trihard$', self.trihard),
            ('^/countdown$', self.overwatch_countdown),
            ('^/poll\s(?P<question>.+)\?\s(?P<options>.*)$', self.poll_views.start_poll),
            ('^/vote\s(?P<number>\d)$', self.poll_views.vote),
            ('^/endpoll$', self.poll_views.end_poll),
            ('^/niggroMode$', self.niggro_mode),
            ('.*(overwatch)|(OVERWATCH)|(Overwatch).*$', self.overwatch_hype),
            ('^/SukDik$', self.sukdik),
        ]

        # spam something every timeout
        threading.Timer(900, self.timer_callback, args=[900]).start()

    def send_text(self, data, to):
        self.interface_layer.toLower(TextMessageProtocolEntity(data, to=to))

    def send_image(self, url, to):
        self.media_views.image_sender.send_by_url(jid=to, file_url=url)

    def timer_callback(self, interval):
        MESSAGE = '''OVERWATCH BEGINS IN: %s.
                     DON\'T BE LATE!''' % get_countdown(2016, 05, 24, 02)

        self.send_text(MESSAGE, '972503305550-1369598727@g.us')
        threading.Timer(interval, self.timer_callback, args=[900]).start()

    def echo(self, message, match):
        self.send_text(match.group("echo_message"), message.getFrom())

    def trihard(self, message, match):
        trihard_emojis = u'\U0001f575'
        trihard_emojis *= 3
        MESSAGE = BOT_SAUL_DICT[randint(0, len(BOT_SAUL_DICT) - 1)] + ' ' + trihard_emojis
        # self.send_image('http://orig09.deviantart.net/5253/f/2012/084/3/3/pewdiepie__try_hard_face_by_arashidaisuki-d4tw9js.png', message.getFrom())
        self.send_text(MESSAGE, message.getFrom())

    def overwatch_countdown(self, message, match):
        MESSAGE = '''OVERWATCH BEGINS IN: %s.
                     DON\'T BE LATE!''' % get_countdown(2016, 05, 24, 02)
        self.send_text(MESSAGE, message.getFrom())

    def overwatch_hype(self, message, match):
        # self.send_image('http://assets.vg247.com/current/2015/09/overwatch.jpg', message.getFrom())
        self.send_text('OVERWATCH HYPEEE!', message.getFrom())
    
    def niggro_mode(self, message, match):
        MESSAGE = NIGGRO_MODE[randint(0, len(NIGGRO_MODE) -1)]
        # self.send_image('https://pbs.twimg.com/media/Bm-Aaf-CEAAHA-P.jpg', message.getFrom())
        self.send_text(MESSAGE, message.getFrom())
        
    def sukdik(self, message, match):
        MESSAGE = SUKDIK[randint(0, len(SUKDIK) -1)]
        self.send_text(MESSAGE, message.getFrom())
