#!/usr/bin/env python3
import os
import sys
import time
import signal
import traceback
import subprocess


DELLUS_API_ARGS = ['gunicorn', '-b 127.0.0.1:9119', '-w 1', 'dellus.rest.wsgi:app']
DELLUSUI_ARGS = ['gunicorn', '-b 0.0.0.0:8000', '-w 1', 'dellusui.wsgi']
process = []


def print_err(proc, timeout=2):
    try:
        print(proc.communicate(timeout=timeout))
    except subprocess.TimeoutExpired:
        pass

try:
    print("Starting API development server at http://127.0.0.1:9119/")
    process.append(subprocess.Popen(DELLUS_API_ARGS, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE))
    # Print any configuration error
    print_err(process[-1])
    print("Starting development server at http://127.0.0.1:8000/")
    os.chdir('dellusui')
    process.append(subprocess.Popen(DELLUSUI_ARGS, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE))
    # Print any configuration error
    print_err(process[-1])
    # Print the logs from process
    counter = 0
    while True:
        # switch between the two process
        counter = counter % 2
        print_err(process[counter])
        counter += 1
except KeyboardInterrupt:
    pass
except Exception as e:
    traceback.print_exc()
finally:
    for proc in process:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
    os.system('cd ..')
    time.sleep(3)
