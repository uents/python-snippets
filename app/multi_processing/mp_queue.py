# -*- coding: utf-8 -*-

import multiprocessing as mp


def f(q_):
    q_.put([42, None, 'hello'])


if __name__ == '__main__':
    q = mp.Queue()
    p = mp.Process(target=f, args=(q,))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    p.join()
