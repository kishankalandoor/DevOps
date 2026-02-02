#!/usr/bin/env python3
"""Split the 15 System Logs terminals into 30 smaller terminals (~50 lines each)."""

import re

with open('logs and journalctl.html', 'r') as f:
    content = f.read()

# Find all System Logs terminals and extract their content
pattern = r'(<!-- System Logs Part (\d+) of 15 -->.*?<div class="terminal-window">.*?<div class="terminal-title">System Logs - Part \d+ of 15</div>.*?<div class="terminal-body">\s*<pre>)(.*?)(</pre>\s*</div>\s*</div>)'

terminals = []
for match in re.finditer(pattern, content, re.DOTALL):
    part_num = int(match.group(2))
    opening = match.group(1)
    log_content = match.group(3)
    closing = match.group(4)
    log_lines = log_content.strip().split('\n')
    terminals.append((part_num, opening, log_lines, closing, match.start(), match.end()))

print(f'Found {len(terminals)} System Logs terminals')

# Split each terminal into 2 parts (~50 lines each)
new_terminals_html = []
total_parts = 0

for part_num, opening, log_lines, closing, start_pos, end_pos in terminals:
    # Split log_lines into chunks of 50
    chunk_size = 50
    chunks = []
    for i in range(0, len(log_lines), chunk_size):
        chunks.append(log_lines[i:i+chunk_size])
    
    # Create new terminals for each chunk
    for chunk_idx, chunk in enumerate(chunks, 1):
        total_parts += 1
        chunk_content = '\n'.join(chunk)
        new_terminal = f'''
        <!-- System Logs Part {total_parts} of 30 -->
        <div class="terminal-window">
            <div class="terminal-titlebar">
                <div class="terminal-dots">
                    <div class="terminal-dot red"></div>
                    <div class="terminal-dot yellow"></div>
                    <div class="terminal-dot green"></div>
                </div>
                <div class="terminal-title">System Logs - Part {total_parts} of 30</div>
            </div>
            <div class="terminal-body">
                <pre>{chunk_content}</pre>
            </div>
        </div>
'''
        new_terminals_html.append(new_terminal)

print(f'Created {total_parts} new terminals')

# Replace all old terminals with new ones
# First, find the position of the first terminal
first_terminal_match = re.search(pattern, content, re.DOTALL)
if not first_terminal_match:
    print('Could not find first terminal')
    exit(1)

# Find the position after the last terminal
last_terminal = terminals[-1]
content_before = content[:first_terminal_match.start()]
content_after = content[last_terminal[5]:]  # After the last terminal

# Build new content
new_content = content_before + ''.join(new_terminals_html) + content_after

# Write the result
with open('logs and journalctl.html', 'w') as f:
    f.write(new_content)

print(f'✓ Split 15 terminals into 30 terminals (~50 lines each)')
print(f'✓ File updated successfully')
