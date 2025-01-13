import random
import sys

def do_sys():
    import platform
    print(sys.platform)
    print(platform.iOS_ver(), platform.machine())
    print(platform.uname(), platform.platform())

def do_lambda():
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

def do_class():
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

def do_mmap():
    import mmap
    # write a simple example file
    with open("hello.txt", "wb") as f:
        f.write(b"Hello Python!\n")

    with open("hello.txt", "r+b") as f:
        # memory-map the file, size 0 means whole file
        mm = mmap.mmap(f.fileno(), 0)
        # read content via standard file methods
        print(mm.readline())  # prints b"Hello Python!\n"
        # read content via slice notation
        print(mm[:5])  # prints b"Hello"
        # update content using slice notation;
        # note that new content must have same size
        mm[6:] = b" world!\n"
        # ... and read again using standard file methods
        mm.seek(0)
        print(mm.readline())  # prints b"Hello  world!\n"
        # close the map
        mm.close()

def do_plot():
    import matplotlib.pyplot as plt

    X = range(10)
    plt.plot(X, [x*x for x in X])
    plt.show()

def main() -> int:
    import shlex
    """Echo the input arguments to standard output"""
    phrase = shlex.join(sys.argv)
    print(phrase)
    prompt = "Enter action (s,l,c,m,p,x): "
    action = input(prompt)
    while (action != 'x'):
        match action:
            case 's':
                do_sys()
            case 'l':
                do_lambda()
            case 'c':
                do_class()
            case 'm':
                do_mmap()
            case 'p':
                do_plot()
            case _:
                pass
        action = input(prompt)
    return 0

if __name__ == '__main__':
    sys.exit(main())