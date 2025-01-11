import random

list1 = random.sample(range(100,200),10)
list2 = random.sample(range(1,100),10)

print(list1,list2)

odd = lambda num: True if (num % 2 == 1) else False

answer1 = []
answer2 = []

for num in list1:
    if not odd(num):
        answer1.append(num)

for num in list2:
    if odd(num):
        answer1.append(num)

answer2 = list(filter(lambda x: x % 2 == 0, list1))
answer2 += list(filter(lambda x: x % 2 != 0, list2))

print("raw1: ", answer1)
print("raw2: ", answer2)

answer1.sort()
answer2.sort()

print("sorted1: ", answer1)
print("sorted2: ", answer2)

class foo:
    """A simple example class"""
    i = 12345

    def f(self):
        return 'hello world'

x = foo
print(foo.__doc__)
print("id(x) = ", id(x), " type(foo) = ", type(foo))
x.counter = 1
while x.counter < 10:
    x.counter = x.counter * 2
print(x.counter)
del x.counter