import logging

logger = logging.getLogger('sfdb')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

file = logging.FileHandler('sfdb.log')
file.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
file.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(file)
