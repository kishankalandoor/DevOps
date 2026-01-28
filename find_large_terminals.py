#!/usr/bin/env python3
import re

with open('logs and journalctl.html', 'r') as f:
    lines = f.readlines()

terminals = []

for i, line in enumerate(lines):
    if 'terminal-title' in line:
        match = re.search(r'<div class="terminal-title">(.*?)</div>', line)
        if match:
            terminal_name = match.group(1)
            for j in range(i, min(i+20, len(lines))):
                if '<pre>' in lines[j]:
                    for k in range(j, min(j+2000, len(lines))):
                        if '</pre>' in lines[k]:
                            content_lines = k - j - 1
                            if content_lines > 50:
                                terminals.append((terminal_name, content_lines, j+1, k+1))
                            break
                    break

print('Terminals with >50 lines:')
for name, count, start, end in sorted(terminals, key=lambda x: x[1], reverse=True):
    print(f'{count:4d} lines: {name[:70]}')
