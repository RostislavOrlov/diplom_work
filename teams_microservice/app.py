import logging
from logging import Logger

import aioredis
from aioredis import Redis
from celery import Celery
from fastapi import FastAPI


class TeamsMicroservice:
    celery: Celery
    logger: Logger
    redis: Redis
    app_fastapi: FastAPI

    def __init__(self, fastapi):
        # TODO: доработать с брокером
        self.celery = Celery('teams', broker='amqp://localhost:15671')
        self.logger = logging.getLogger('teams_microservice')
        self.redis = aioredis.from_url('redis://localhost:6378')
        self.app_fastapi = fastapi
        # self.rabbitmq = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        # self.rabbitmq_channel = self.rabbitmq.channel()
        # self.posts_channel = self.rabbitmq_channel.queue_declare(queue='posts')
