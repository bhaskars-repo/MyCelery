#
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   17 Sep 2020
#

BROKER_URL = 'amqp://celery:s3cr3t@192.168.1.23:5672/celery_vhost'
CELERY_RESULT_BACKEND = 'redis://192.168.1.31:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_INCLUDE = ['MyCelery.celery_tasks']
CELERY_ACKS_LATE = True
CELERY_TASK_ROUTES = {
    'MyCelery.celery_tasks.test_task': {'queue': 'test_task.Q', },
    'MyCelery.celery_tasks.get_rate': {'queue': 'get_rate.Q', },
    'MyCelery.celery_tasks.get_exch_rate': {'queue': 'get_rate.Q', },
    'MyCelery.celery_tasks.get_avg_exch_rate': {'queue': 'get_rate.Q', },
}
