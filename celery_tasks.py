#
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   17 Sep 2020
#

import random
import time

from datetime import datetime
from celery.utils.serialization import jsonify

from MyCelery.celery_base import celery_app

crypto_fx = {'BLU': 0.0095,
             'RED': 0.0028}

exchange_diff = {'CAT-BLU': [0.0001, 0.0002, 0.0003, 0.0004, 0.0005],
                 'CAT-RED': [0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008],
                 'DOG-BLU': [0.0002, 0.0004],
                 'DOG-RED': [0.0002, 0.0004, 0.0006, 0.0008],
                 'FOX-BLU': [0.0001, 0.0003, 0.0005],
                 'FOX-RED': [0.0001, 0.0003, 0.0005, 0.0007]}

random.seed()


@celery_app.task(name='MyCelery.celery_tasks.test_task')
def test_task():
    """
    Task used for testing the setup
        :return: json string with a timestamp field
    """
    time.sleep(0.1)
    return jsonify({"timestamp": datetime.now()})


@celery_app.task(name='MyCelery.celery_tasks.get_rate')
def get_rate(crypto):
    """
    Task used to get the lowest rate of two fictitious crypto coins - BLU and RED from the fictitious market
    providers - CAT, DOG, and FOX
        :param crypto: string with value 'BLU' or 'RED'
        :return: json string with the rate from the provider
    """
    rb = crypto_fx[crypto] - random.choice(exchange_diff['CAT-' + crypto])
    time.sleep(0.05)
    rf = crypto_fx[crypto] - random.choice(exchange_diff['DOG-' + crypto])
    time.sleep(0.05)
    rl = crypto_fx[crypto] - random.choice(exchange_diff['FOX-' + crypto])
    time.sleep(0.05)

    val, idx = min((val, idx) for (idx, val) in enumerate([rb, rf, rl]))

    return jsonify({'crypto': crypto, 'rate': val, 'provider': ['CAT', 'DOG', 'FOX'][idx]})


@celery_app.task(name='MyCelery.celery_tasks.get_exch_rate')
def get_exch_rate(exch, crypto):
    """
    Task to get the current rate for a given fictitious exchange and fictitious crypto coin
        :param exch: string with one of the values 'CAT', 'DOG', or 'FOX'
        :param crypto: string with value 'BLU' or 'RED'
        :return: json string with the rate from the provider
    """
    if datetime.today().second % 2 == 0:
        rate = crypto_fx[crypto] - random.choice(exchange_diff[exch + '-' + crypto])
    else:
        rate = crypto_fx[crypto] + random.choice(exchange_diff[exch + '-' + crypto])
    time.sleep(0.5)

    return jsonify({'provider': exch, 'crypto': crypto, 'rate': rate})


@celery_app.task(name='MyCelery.celery_tasks.get_avg_exch_rate')
def get_avg_exch_rate(exch_rates):
    """
    Task that takes in an json object with array of rates from a provider and computes the average rate
        :param exch_rates: json object containing an array of rates from a provider
        :return: json string with the average rate from the provider
    """
    acc = 0.0
    for elem in exch_rates:
        acc += elem['rate']
    avg = acc / len(exch_rates)
    time.sleep(0.5)

    return jsonify({'provider': exch_rates[0]['provider'], 'crypto': exch_rates[0]['crypto'], 'average': avg})
