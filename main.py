from datetime import datetime

import pytest


def add(a, b):
    c = a + b
    return c


d = add(1, 2)
print(d)
