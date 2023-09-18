"""
Useful wrappers for GET and POST calls

Author: Darren Li
"""
import requests
from math import exp
from time import sleep
from random import uniform


import WebTools as wt

__all__ = ['get_', 'post_']

DEFAULT_HEADERS = {
    'User-Agent': wt.get_user_agent()
}
DEFAULT_DATA = {}


def rand_wait(wait_minimum=5, exp_max=10):
    """
    Wait function, using random time based on:
        wait_minimum + exp([0, exp_max]) 
    
    """
    rand_exp = uniform(0, float(exp_max))
    time = wait_minimum + exp(rand_exp)
    sleep(time)


def get_(url, headers=DEFAULT_HEADERS, retries=wt.MAX_RETRIES,
         timeout=wt.TIMEOUT):
    """Wrapper for requests"""
    rand_wait()

    for i in range(retries, 0 , -1):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            if resp.ok:
                return resp
        except requests.exceptions.Timeout:
            print('Timed out')
        except Exception as e:
            print(e)
        print(f"Retries left: {i}")
    raise requests.RequestException('')


def post_():
    pass
