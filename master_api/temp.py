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
import matplotlib.pyplot as plt
import io

# Global Declarations
performance_log_path = './performance_log.csv'
primes_list_path = './updated_primes_list.txt'
log_interval = 60  # in seconds
get_primes_list_interval = 120  # in seconds
tz = pytz.timezone('Asia/Karachi')


def plot_performance():
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

        plt.show()
