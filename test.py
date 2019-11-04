import heapq
import random
import numpy as np


import heapq
import random

def a_res(samples, m):
    """
    :samples: [(item, weight), ...]
    :k: number of selected items
    :returns: [(item, weight), ...]
    """

    heap = [] # [(new_weight, item), ...]
    for sample in samples:
        wi = sample[1]
        ui = random.uniform(0, 1)
        ki = ui ** (1/wi)

        if len(heap) < m:
            heapq.heappush(heap, (ki, sample))
        elif ki > heap[0][0]:
            heapq.heappush(heap, (ki, sample))

            if len(heap) > m:
                heapq.heappop(heap)

    return [item[1] for item in heap]

def a_expj(samples, m):
    """
    :samples: [(item, weight), ...]
    :k: number of selected items
    :returns: [(item, weight), ...]
    """

    heap = [] # [(new_weight, item), ...]

    Xw = None
    Tw = 0
    w_acc = 0
    for sample in samples:
        if len(heap) < m:
            wi = sample[1]
            ui = random.uniform(0, 1)
            ki = ui ** (1/wi)
            heapq.heappush(heap, (ki, sample))
            continue

        if w_acc == 0:
            Tw = heap[0][0]
            r = random.uniform(0, 1)
            Xw = np.log(r)/np.log(Tw)

        wi = sample[1]
        if w_acc + wi < Xw:
            w_acc += wi
            continue
        else:
            w_acc = 0

        tw = Tw ** wi
        r2 = random.uniform(tw, 1)
        ki = r2 ** (1/wi)
        heapq.heappop(heap)
        heapq.heappush(heap, (ki, sample))

    return [item[1] for item in heap]
overall = [('a', 10), ('b', 20), ('c', 50), ('d', 100), ('e', 200)]

def test_weighted_sampling(func, k):
    stat = {}
    for i in range(100000):
        sampled = func(overall, k)
        for item in sampled:
            if item[0] not in stat:
                stat[item[0]] = 0
            stat[item[0]] += 1
    total = stat['a']
    for a in stat:
        stat[a] = float(stat[a])/float(total)
    print(stat)
if __name__ == '__main__':
    test_weighted_sampling(a_res, 1)
    test_weighted_sampling(a_res, 2)
    test_weighted_sampling(a_res, 3)
    test_weighted_sampling(a_res, 4)
    test_weighted_sampling(a_res, 5)
