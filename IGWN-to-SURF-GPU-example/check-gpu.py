#!/bin/env python
# -*- coding: utf-8 -*-

""" check-gpu.py:  Check whether a GPU is found.
    2023-11-24, MvdS: initial version.
"""

import datetime

print('Start: ', datetime.datetime.utcnow(), 'UTC')

try:
    import torch
except Exception as e:
    print('PyTorch could not be imported')
    print(e)
    exit(1)

print('Middle: ', datetime.datetime.utcnow(), 'UTC')

# Check whether CUDA is available:
if torch.cuda.is_available():
    print('GPUs found:')
    for i in range(torch.cuda.device_count()):
        print(torch.cuda.get_device_properties(i).name)    
else:
    print('No GPU was found!')

print('End: ', datetime.datetime.utcnow(), 'UTC')

