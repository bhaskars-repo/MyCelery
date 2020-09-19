#
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   17 Sep 2020
#

from celery import Celery
from MyCelery import celery_config

celery_app = Celery('celery_tasks')
celery_app.config_from_object(celery_config)
