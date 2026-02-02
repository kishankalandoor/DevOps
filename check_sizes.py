#!/usr/bin/env python3
import re

with open('logs and journalctl.html', 'r') as f:
    lines = f.readlines()

print("System Logs terminal sizes:")
for i in range(1, 16):
    for j, line in enumerate(lines):
        if f'System Logs - Part {i} of 15' in line and 'terminal-title' in line:
            # Find the pre tag
            for k in range(j, min(j+20, len(lines))):
                if '<pre>' in lines[k]:
                    # Find closing pre
                    for m in range(k, min(k+200, len(lines))):
                        if '</pre>' in lines[m]:
                            content_lines = m - k - 1
                            print(f'Part {i:2d}: {content_lines:3d} lines')
                            break
                    break
            break
