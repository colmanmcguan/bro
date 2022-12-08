import os
import sys
import multiprocessing as mp
import numpy as np 

def load_trace(file):
    return np.loadtxt(file, delimiter="\t")

def simulate(f):
    trace = load_trace(f)
    outgoing = trace[np.where(trace[:,1] == 777)]
    incoming = trace[np.where(trace[:,1] == -777)]
    outgoing = outgoing[outgoing[:,0].argsort(kind="mergesort")]
    incoming = incoming[incoming[:,0].argsort(kind="mergesort")]
    if len(outgoing) == 0:
        out_rng = 0
    else:
        q75, q25 = np.percentile(outgoing[:,0], [75, 25])
        out_rng = q75 -q25
    if len(incoming) == 0:
        in_rng = 0
    else:
        q75, q25 = np.percentile(incoming[:,0], [75, 25])
        in_rng = q75 -q25
    return [out_rng, in_rng]

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
    arr = list(arr[0]) + list(arr[1])
    arr = np.array(arr)
    print("mean: {}\nstd dev: {}\nmedian: {}".format(arr.mean(), arr.std(), np.median(arr)))
    print("max: {}".format(arr.max()))
