import io
import matplotlib.pyplot as plt
from django.shortcuts import render
from django.http import HttpResponse
import requests
import pandas as pd
import os
import math
import time
import threading
import datetime
import pytz
import matplotlib
matplotlib.use('Agg')

# Global Declarations
performance_log_path = './performance_log.csv'
primes_list_path = './updated_primes_list.txt'
log_interval = 60  # in seconds
get_primes_list_interval = 120  # in seconds
tz = pytz.timezone('Asia/Karachi')

# Utility Functions


def log_performance():
    res = requests.get(f'http://127.0.0.1:8001/api/monitor/1')
    performance = res.json()
    performance['timestamp'] = datetime.datetime.now(tz)

    if not os.path.exists(performance_log_path):
        os.makedirs(os.path.dirname(performance_log_path), exist_ok=True)
        log = pd.DataFrame(data=[performance])
        log.to_csv(performance_log_path, index=False)
    else:
        logs = pd.read_csv(performance_log_path)
        new_log = pd.DataFrame(data=[performance])
        updated_logs = pd.concat([logs, new_log], ignore_index=True, axis=0)
        updated_logs.to_csv(performance_log_path, index=False)


def get_latest_primes_list():

    if not os.path.exists(performance_log_path):
        os.makedirs(os.path.dirname(performance_log_path), exist_ok=True)
    updated_primes = []
    res1 = requests.get(f'http://127.0.0.1:8001/api/get')
    res2 = requests.get(f'http://127.0.0.1:8002/api/get')
    res3 = requests.get(f'http://127.0.0.1:8003/api/get')

    updated_primes = res1.json()['primes'] + \
        res2.json()['primes']+res3.json()['primes']

    with open(primes_list_path, 'w') as f:
        for prime in updated_primes:
            f.write("%d " % prime)

    f.close()


def periodic(interval, func):
    while True:
        time.sleep(interval)
        func()


# Create your views here.


def invoke(request):
    prime_range = math.floor(10**12/3)
    requests.get(f'http://127.0.0.1:8001/api/generate/1/{prime_range}')
    requests.get(
        f'http://127.0.0.1:8002/api/generate/{prime_range+1}/{prime_range*2}')
    requests.get(
        f'http://127.0.0.1:8003/api/generate/{prime_range*2+1}/{(prime_range*3)+1}')

    thread = threading.Thread(
        target=periodic, args=(log_interval, log_performance))
    thread.daemon = True
    thread.start()

    thread1 = threading.Thread(target=periodic, args=(
        get_primes_list_interval, get_latest_primes_list))
    thread1.daemon = True
    thread1.start()

    return HttpResponse('Master Service Invoked.....')


def plot_performance(request):
    if os.path.exists(performance_log_path):
        df = pd.read_csv(performance_log_path)

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)

        fig, ax = plt.subplots()
        ax.plot(df['cpu_usage'], label='CPU Usage')
        ax.plot(df['memory_usage'], label='Memory Usage')
        ax.set_xlabel('Timestamp')
        ax.set_ylabel('Usage (%)')
        ax.set_title('CPU and Memory Usage')
        ax.grid(True, linestyle='--')
        ax.legend()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        return HttpResponse(buffer, content_type='image/png')
    else:
        return HttpResponse('Performance does not exist yet. Invoke master first or wait for master to create logs...')
