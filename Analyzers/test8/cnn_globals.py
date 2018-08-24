from nn_logging import getLogger
logger = getLogger()

# ______________________________________________________________________________
# Globals

infile_images = '../test7/histos_tbe.17a.npz'


# ______________________________________________________________________________
# Import all the libs
import os
import sys
os.environ['KERAS_BACKEND'] = 'tensorflow'
OLD_STDOUT = sys.stdout

logger.info('Using cmssw {0}'.format(os.environ['CMSSW_VERSION']))

import numpy as np
np.random.seed(2023)
logger.info('Using numpy {0}'.format(np.__version__))

import tensorflow as tf
logger.info('Using tensorflow {0}'.format(tf.__version__))

from tensorflow import keras as tf_keras
K = tf_keras.backend
logger.info('Using keras {0}'.format(tf_keras.__version__))
logger.info('.. list devices: {0}'.format(K.get_session().list_devices()))

import scipy
logger.info('Using scipy {0}'.format(scipy.__version__))

import sklearn
logger.info('Using sklearn {0}'.format(sklearn.__version__))

import matplotlib.pyplot as plt
#from matplotlib import colors
#%matplotlib inline
