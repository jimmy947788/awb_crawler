import os
import sys
import pathlib
import logging
import logging.handlers as handlers

def init_logger(worker_folder, appname):
   
    log_folder = os.path.join(worker_folder, 'logs')
    pathlib.Path(log_folder).mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(appname)
    logger.setLevel(logging.DEBUG)

    ## Here we define our formatter
    formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
    #=f'%(asctime)s %(levelname)s %(name)s %(threadName)s [worker]: %(message)s')

    logHandler = handlers.TimedRotatingFileHandler(os.path.join(log_folder,  f'{appname}.log'), when='d', interval=1, backupCount=0)
    logHandler.setLevel(logging.DEBUG)
    logHandler.setFormatter(formatter)

    errorLogHandler = handlers.RotatingFileHandler(os.path.join(log_folder, f'{appname}-error.log'), maxBytes=5000, backupCount=0)
    errorLogHandler.setLevel(logging.ERROR)
    errorLogHandler.setFormatter(formatter)

    logger.addHandler(logHandler)
    logger.addHandler(errorLogHandler)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    return logger