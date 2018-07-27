import os, platform, logging


fichero_log = ''

def crear():

	global fichero_log

	if platform.platform().startswith('Windows'):
	    fichero_log = os.path.join(os.getenv('HOMEDRIVE'), 
	                               os.getenv("HOMEPATH"),
	                               'lyndor.log')
	else:
	    fichero_log = os.path.join(os.getenv('HOME'), 'lyndor.log')

	logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s : %(levelname)s : %(message)s',
                    filename = fichero_log,
                    filemode = 'w')

	# Ejemplos
	# logging.debug('Comienza el programa')
	# logging.error('Creando fichero')
	# logging.info('Procesando con normalidad')
	# logging.warning('Advertencia')


