#!/usr/bin/env python3
with open('logs and journalctl.html', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'View Syslog - cat /var/log/syslog' in line:
        print(f'View Syslog title at line {i+1}')
        for j in range(i, min(i+50, len(lines))):
            if '<pre>' in lines[j]:
                print(f'PRE opens at line {j+1}')
                for k in range(j, len(lines)):
                    if '</pre>' in lines[k]:
                        print(f'PRE closes at line {k+1}')
                        print(f'Lines between: {k-j-1}')
                        break
                break
        break

# Find Part 1 of 15
for i, line in enumerate(lines):
    if 'System Logs - Part 1 of 15' in line and 'terminal-title' in line:
        print(f'\nPart 1 of 15 at line {i+1}')
        break
