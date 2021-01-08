import os

RABBITMQ_EXCHANGE_NAME = os.environ.get(
    'RABBITMQ_EXCHANGE_NAME') if 'RABBITMQ_EXCHANGE_NAME' in os.environ else 'chainchomp_rabbitmq_exchange'
