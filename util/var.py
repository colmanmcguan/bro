import os
import sys
import multiprocessing as mp
import numpy as np 

def load_trace(f):
    return np.loadtxt(file, delimiter="\t")

def simulate(f):
    trace = load_trace(f)
    trace = trace[trace[:,0].argsort(kind="mergesort")]
    lastpkt = trace[-1][0]
    dummy = trace[np.where(abs(trace[:,1]) == 777)]
    return dummy[:,0]

def parallel(flist, n_jobs=25):
    pool = mp.Pool(n_jobs)
    arr = pool.map(simulate, flist)
    return arr

if __name__ == '__main__':
    flist  = []
    for f in os.listdir(sys.argv[1]):
        flist.append(os.path.join(sys.argv[1], f))

    arr = parallel(flist)
    arr = list(zip(*arr))
    narr = []
    for a in arr:
        narr = narr + list(a)
    rr = np.array(narr)
    print("median timestamp: {}".format(np.median(arr)))
    print("mean timestamp: {}".format(arr.mean()))
    print("coef var: {}".format(arr.std() / arr.mean()))

