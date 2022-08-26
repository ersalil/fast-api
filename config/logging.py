import logging, logging.config
import contextvars, uuid


log_format = '''[%(asctime)s] {%(pathname)s:%(lineno)d} %(white)s|%(name)s|-
%(log_color)s%(levelname)s: %(blue)s%(message)s
'''

LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            '()': 'colorlog.ColoredFormatter',
            'format': log_format,
            'datefmt': None,
            'reset': True,
            'log_colors': {
                'DEBUG':    'cyan',
                'INFO':     'green',
                'WARNING':  'yellow',
                'ERROR':    'red',
                'CRITICAL': 'red,bg_white',
            },
            'secondary_log_colors': {},
            'style': '%',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default'
        },
        'file': {
            # The values below are popped from this dictionary and
            # used to create the handler, set the handler's level and
            # its formatter.
            '()': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            # The values below are passed to the handler creator callable
            # as keyword arguments.
            'filename': 'logfile.log',
            'mode': 'a',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'production': {
            'handlers': ['console'],
            'formatter': 'default',
            'propagate': False,
            'level': 'DEBUG',
        },
        'development': {
            'handlers': ['console'],
            'formatter': 'default',
            'propagate': False,
            'level': 'DEBUG',
        }
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['console']
    }
}

logging.config.dictConfig(LOGGING)

request_id_contextvar = contextvars.ContextVar("request_id", default=None)

def createRequestIdContextvar(id=str(uuid.uuid4())):
    return request_id_contextvar.set(id)

def getRequestId():
    return request_id_contextvar.get()


class Log:
    def __init__(self):
        self.logger = logging.getLogger('development')
        self.logger.info('Logger initialized')

    def info(self, msg, data="None"):
        self.logger.info(f"{getRequestId()} - {msg} - {data}")

    def error(self, msg, e="None"):
        self.logger.error(f"{getRequestId()} - {msg} - {e}")

    def debug(self, msg):
        self.logger.debug(f"{getRequestId()} - {msg}")

    def warning(self, msg, data="None"):
        self.logger.warning(f"{getRequestId()} - {msg} - {data}")

    def critical(self, msg):
        self.logger.critical(msg)

    def exception(self, msg):
        self.logger.exception(msg)

log = Log()