import re
import random
import time

from django.test import TestCase

# Create your tests here.

# 测试

r = 100000
count = 0

s1 = time.time()
for i in range(r):
    if random.random() > 0.5:
        count += 1
print(count/r)
e1 = time.time()

s2 = time.time()
rst = [1 for i in range(r) if random.random() > 0.5]
print(sum(rst)/r)
e2 = time.time()

print(e1-s1)
print(e2-s2)

# 在本地的修改
