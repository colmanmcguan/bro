import os
import sys
import multiprocessing as mp
import numpy as np 

def load_trace(f):
    return np.loadtxt(f, delimiter="\t")

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
    fdir = os.path.join("defended", sys.argv[1])
    flist  = []
    for f in os.listdir(fdir):
        flist.append(os.path.join(fdir, f))

    arr = parallel(flist)
    arr = list(zip(*arr))
    narr = []
    for a in arr:
        narr = narr + list(a)
    arr = np.array(narr)
    print("{} timestamps".format(sys.argv[1]))
    print("================================")
    print("median timestamp:\t{:.4f}".format(np.median(arr)))
    print("mean timestamp:\t\t{:.4f}".format(arr.mean()))
    print("coef. of var.:\t\t{:.4f}".format(arr.std() / arr.mean()))
    print()
