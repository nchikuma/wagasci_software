#!/usr/bin/env python 

import os
file_path="test.py"

time = int(os.stat(file_path).st_mtime)
print time
