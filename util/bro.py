import os
import sys
import time
import configparser
import multiprocessing as mp
import numpy as np 

def load_trace(f):
    return np.loadtxt(f, delimiter='\t')

def dump_trace(trace, f):
    global defended
    with open(os.path.join(defended, f), "w") as fp:
        for pkt in trace:
            fp.write("{:.4f}\t{}\n".format(pkt[0], pkt[1]))

def run_defense(f):
    trace = load_trace(f)
    trace = brain_surgery(trace)
    f = f.split('/')[-1]
    dump_trace(trace, f)

def get_injection():
    global client_max
    global server_max
    global client_min
    global server_min
    global a_max
    global a_min
    global b_max
    global b_min

    # get padding window
    client_win = np.random.uniform(min_win, max_win)
    server_win = np.random.uniform(min_win, max_win)

    # get number of dummys
    client_num = np.random.randint(client_min, client_max)
    server_num = np.random.randint(server_min, server_max)

    # beta params
    client_a = np.random.uniform(a_min, a_max)
    client_b = np.random.uniform(b_min, b_max)
    server_a = np.random.uniform(a_min, a_max)
    server_b = np.random.uniform(b_min, b_max)

    # sample timestamps
    client = np.random.beta(client_a, client_b, client_num) * client_win
    server = np.random.beta(server_a, server_b, server_num) * server_win
    client = np.reshape(client, (len(client),1))
    server = np.reshape(server, (len(server),1))
    client = np.concatenate((client, np.ones((len(client),1))), axis=1)
    server = np.concatenate((server, -1*np.ones((len(server),1))), axis=1)

    # merge back together
    injection = np.concatenate((client, server))
    injection = injection[injection[:,0].argsort(kind="mergesort")]
    return injection

def brain_surgery(trace):
    injection = get_injection()
    last_pkt = trace[-1][0]
    client_reals = trace[np.where(trace[:,1] == 1)]
    server_reals = trace[np.where(trace[:,1] == -1)]
    client_dummys = injection[np.where(injection[:,1] == 1)]
    client_dummys = client_dummys[np.where(client_dummys[:,0] <= last_pkt)]
    server_dummys = injection[np.where(injection[:,1] == -1)]
    server_dummys[:,0] += server_reals[0][0]
    server_dummys = server_dummys[np.where(server_dummys[:,0] <= last_pkt)]

    # add dummy packets
    noisy_trace = np.concatenate((client_reals, client_dummys, server_reals, server_dummys), axis=0)
    noisy_trace = noisy_trace[noisy_trace[:,0].argsort(kind="mergesort")]

    return noisy_trace

def parallel(flist, n_jobs=25):
    pool = mp.Pool(n_jobs)
    pool.map(run_defense, flist)

if __name__ == '__main__':
    # defense config/parameters
    global conf         # defense configuration
    global min_win      # minimum window size
    global max_win      # maximum window size
    global client_min 
    global client_max
    global server_min
    global server_max
    global a_min        # minimum value for alpha parameter
    global a_max        # maximum value for alpha parameter
    global b_min        # minimum value for beta parameter
    global b_max        # maximum value for beta parameter

    # trace locations
    global undefended
    global defended

    if len(sys.argv) != 2:
        print("usage: python3 bro.py <config>")
        sys.exit(1)

    conf = sys.argv[1]
    conf_parser = configparser.RawConfigParser()
    conf_parser.read("./util/config.ini")

    config = dict(conf_parser._sections[conf])

    client_min = int(config.get("client_min", 0))
    client_max = int(config.get("client_max", 0))
    server_min = int(config.get("server_min", 0))
    server_max = int(config.get("server_max", 0))
    min_win = float(config.get('min_win',14))
    max_win = float(config.get('max_win',14))
    a_min = float(config.get("a_min",0))
    a_max = float(config.get("a_max",0))
    b_min = float(config.get("b_min",0))
    b_max = float(config.get("b_max",0))

    # info
    print("parameters for {}".format(conf))
    print("================================")
    print("parameter\tvalue")
    print("--------------------------------")
    print("client_min\t{}".format(client_min))
    print("client_max\t{}".format(client_max))
    print("server_min\t{}".format(server_min))
    print("server_max\t{}".format(server_max))
    print("min_win\t\t{}".format(min_win))
    print("max_win\t\t{}".format(max_win))
    print("a_min\t\t{}".format(a_min))
    print("a_max\t\t{}".format(a_max))
    print("b_min\t\t{}".format(b_min))
    print("b_max\t\t{}".format(b_max))

    # setup directories
    undefended = "./log/undefended/"
    defended = "./defended/{}".format(conf)
    if not os.path.exists(defended):
        os.makedirs(defended)

    flist  = []
    for f in os.listdir(undefended):
        flist.append(os.path.join(undefended, f))

    # init run directories
    print("traces are dumped to {}".format(defended))
    start = time.time()
    parallel(flist)
    print("time: {}\n".format(time.time()-start))
