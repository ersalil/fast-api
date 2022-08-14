import logging, logging.config
import contextvars, uuid, time
from fastapi import Request

logging.config.fileConfig('logging.conf')

request_id_contextvar = contextvars.ContextVar("request_id", default=None)

def createRequestIdContextvar():
    return request_id_contextvar.set(str(uuid.uuid4()))

def getRequestId():
    return request_id_contextvar.get()

class Log:
    def __init__(self):
        self.logger = logging.getLogger('emb-mon-log')
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

async def logGenerator(request: Request):
    with open('./logfile.log', 'r') as file:
        log.debug("Client Connected")
        for line in file.readlines()[::-1]:
            if await request.is_disconnected():
                log.debug("Client disconnected")
                break
            yield line
