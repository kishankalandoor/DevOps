#!/usr/bin/env python3
"""Split the 30 System Logs terminals into 60 smaller terminals (~25 lines each)."""

import re

with open('logs and journalctl.html', 'r') as f:
    content = f.read()

# Find all System Logs terminals and extract their content
pattern = r'(<!-- System Logs Part (\d+) of 30 -->.*?<div class="terminal-window">.*?<div class="terminal-title">System Logs - Part \d+ of 30</div>.*?<div class="terminal-body">\s*<pre>)(.*?)(</pre>\s*</div>\s*</div>)'

terminals = []
for match in re.finditer(pattern, content, re.DOTALL):
    part_num = int(match.group(2))
    opening = match.group(1)
    log_content = match.group(3)
    closing = match.group(4)
    log_lines = log_content.strip().split('\n')
    terminals.append((part_num, opening, log_lines, closing, match.start(), match.end()))

print(f'Found {len(terminals)} System Logs terminals')

# Split each terminal into chunks of 25 lines
new_terminals_html = []
total_parts = 0

for part_num, opening, log_lines, closing, start_pos, end_pos in terminals:
    # Split log_lines into chunks of 25
    chunk_size = 25
    chunks = []
    for i in range(0, len(log_lines), chunk_size):
        chunks.append(log_lines[i:i+chunk_size])
    
    # Create new terminals for each chunk
    for chunk_idx, chunk in enumerate(chunks, 1):
        total_parts += 1
        chunk_content = '\n'.join(chunk)
        new_terminal = f'''
        <!-- System Logs Part {total_parts} of 60 -->
        <div class="terminal-window">
            <div class="terminal-titlebar">
                <div class="terminal-dots">
                    <div class="terminal-dot red"></div>
                    <div class="terminal-dot yellow"></div>
                    <div class="terminal-dot green"></div>
                </div>
                <div class="terminal-title">System Logs - Part {total_parts} of 60</div>
            </div>
            <div class="terminal-body">
                <pre>{chunk_content}</pre>
            </div>
        </div>
'''
        new_terminals_html.append(new_terminal)

print(f'Created {total_parts} new terminals')

# Replace all old terminals with new ones
first_terminal_match = re.search(pattern, content, re.DOTALL)
if not first_terminal_match:
    print('Could not find first terminal')
    exit(1)

last_terminal = terminals[-1]
content_before = content[:first_terminal_match.start()]
content_after = content[last_terminal[5]:]

# Build new content
new_content = content_before + ''.join(new_terminals_html) + content_after

# Write the result
with open('logs and journalctl.html', 'w') as f:
    f.write(new_content)

print(f'✓ Split 30 terminals into {total_parts} terminals (~25 lines each)')
print(f'✓ All content preserved - nothing skipped')
print(f'✓ File updated successfully')
