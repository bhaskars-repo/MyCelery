#
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   17 Sep 2020
#

import sys

from MyCelery.celery_tasks import test_task, get_rate


def print_details(name, res):
    """
    Prints the details of the response object of the submitted task
        :param name: name of the approach used to submit the task (delay or apply_async)
        :param res: response object of type AsyncResult
        :return: None
    """
    print(f'{name} res type: {type(res)}')
    print(f'{name} test_task ready ?: {res.ready()}')
    print(f'{name} test_task status: {res.status}')
    print(f'{name} response: {res.get()}')
    print(f'{name} test_task ready ?: {res.ready()}')
    print(f'{name} test_task status: {res.status}')


"""
Main program - if the specified argument is 'test', invoke the test_task. Else, if the specified argument is 'rate'
invoke the get_rate task
"""
if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in ['test', 'rate']:
        print('Usage: python celery_client.py <test | rate>')
        sys.exit(1)

    if sys.argv[1] == 'test':
        print('1. test_task via delay ...')

        res1 = test_task.delay()

        print_details('delay', res1)

        print('2. test_task via apply_async ...')

        res2 = test_task.apply_async(queue='test_task.Q')

        print_details('apply_async', res2)
    else:
        for i in range(1, 6):
            print(f'Loop - # {i}')

            res1 = get_rate.apply_async(queue='get_rate.Q', args=('BLU',))
            json1 = res1.get(timeout=5.0)

            print(f'{i} BLU :: {json1}')

            res2 = get_rate.apply_async(queue='get_rate.Q', args=('RED',))
            json2 = res2.get(timeout=5.0)

            print(f'{i} RED :: {json2}')
