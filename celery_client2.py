#
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   17 Sep 2020
#

from celery import chain, group

from MyCelery.celery_tasks import get_exch_rate, get_avg_exch_rate

"""
Main program that demonstrates how one could create complex pipelines using the group and chain tasks
"""
if __name__ == '__main__':
    group_inst = group(get_exch_rate.s('FOX', 'RED'),
                       get_exch_rate.s('FOX', 'RED'),
                       get_exch_rate.s('FOX', 'RED'))

    print(f'group_inst = {group_inst}')
    res = group_inst.apply_async(queue='get_rate.Q')
    print(f'group res type: {type(res)}')
    print(f'group ready ?: {res.ready()}')
    print(f'response: {res.get()}')
    print(f'group ready ?: {res.ready()}')

    chain_inst = chain(group(get_exch_rate.s('DOG', 'BLU'),
                             get_exch_rate.s('DOG', 'BLU'),
                             get_exch_rate.s('DOG', 'BLU')),
                       get_avg_exch_rate.s())

    print(f'chain_inst = {chain_inst}')
    res2 = chain_inst.apply_async(queue='get_rate.Q')
    print(f'chain res type: {type(res2)}')
    print(f'chain ready ?: {res2.ready()}')
    print(f'response: {res2.get()}')
    print(f'chain ready ?: {res2.ready()}')
