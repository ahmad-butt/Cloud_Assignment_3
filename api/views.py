from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import threading
import math
import queue
import psutil

# Global Declarations
primes = queue.Queue()
lock = threading.Lock()

# Utility Functions


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def generate_primes(start, end):
    for num in range(start, end + 1):
        if is_prime(num):
            with lock:
                primes.put(num)


def start_generation(start, end):
    t = threading.Thread(target=generate_primes, args=(start, end))
    t.start()

# Create your views here.


def generate(request, start, end):
    global primes
    primes = queue.Queue()
    start_generation(start, end)
    return HttpResponse(F"Generating Prime Numbers from {start} to {end}...")


@api_view(['GET'])
def monitor(request, k):
    cpu_usage = psutil.cpu_percent(interval=k, percpu=False)
    memory_usage = psutil.virtual_memory().percent

    context = {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage
    }

    return Response(context)


def get(request):
    with lock:
        return JsonResponse({"primes": list(primes.queue)})
