# Settings file
import os

# Paths
BASE_PATH = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_PATH, os.path.pardir))

INPUT_FIELDS = ['order_id', 'timeval', 'stock', 'action', 'quantity', 'price']