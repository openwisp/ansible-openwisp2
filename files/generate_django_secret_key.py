#!/usr/bin/env python3
"""
Pseudo-random django secret key generator
"""
from __future__ import print_function
import random

chars = 'abcdefghijklmnopqrstuvwxyz' \
        'ABCDEFGHIJKLMNOPQRSTUVXYZ' \
        '0123456789' \
        '#()^[]-_*%&=+/'

SECRET_KEY = ''.join([random.SystemRandom().choice(chars) for i in range(50)])

print(SECRET_KEY)
