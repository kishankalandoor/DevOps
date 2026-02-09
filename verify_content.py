import re

# Read source
with open('/Applications/XAMPP/xamppfiles/htdocs/DevOps/bash_history_backup.html', 'r', encoding='utf-8') as f:
    source = f.read()

# Read output
with open('/Applications/XAMPP/xamppfiles/htdocs/DevOps/bash activities.html', 'r', encoding='utf-8') as f:
    output = f.read()

# Extract source terminal
source_match = re.search(r'Last login:.*?(?=\[Message clipped\])', source, re.DOTALL)
source_terminal = source_match.group(0) if source_match else ''

# Extract all output terminal blocks
output_blocks = re.findall(r'<pre>(.*?)</pre>', output, re.DOTALL)
output_terminal = '\n'.join(output_blocks)

print('=== SOURCE SAMPLE (first 10 lines) ===')
for i, line in enumerate(source_terminal.split('\n')[:10], 1):
    print(f'{i}: {line[:80]}')

print('\n=== OUTPUT SAMPLE (first 10 lines) ===')
for i, line in enumerate(output_terminal.split('\n')[:10], 1):
    print(f'{i}: {line[:80]}')

print('\n=== LAST 10 LINES COMPARISON ===')
source_lines = source_terminal.split('\n')
output_lines = output_terminal.split('\n')

print('Source (last 10):')
for i, line in enumerate(source_lines[-10:], len(source_lines)-9):
    print(f'{i}: {line[:80]}')

print('\nOutput (last 10):')
for i, line in enumerate(output_lines[-10:], len(output_lines)-9):
    print(f'{i}: {line[:80]}')

print(f'\n=== STATISTICS ===')
print(f'Source lines: {len(source_lines)}')
print(f'Output lines: {len(output_lines)}')
print(f'Content match: {source_terminal == output_terminal}')
print(f'Source chars: {len(source_terminal)}')
print(f'Output chars: {len(output_terminal)}')
