#!/usr/bin/env python3
"""Split the large System Logs terminal into 15 separate terminals."""

with open('logs and journalctl.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the "System Logs - Detailed Output" terminal
start_marker = '<!-- Additional System Logs Terminal -->'
title_marker = 'System Logs - Detailed Output'

start_pos = content.find(start_marker)
title_pos = content.find(title_marker)

if start_pos == -1 or title_pos == -1:
    print("Could not find the System Logs terminal")
    exit(1)

# Find where the <pre> tag opens (after the title)
pre_start = content.find('<pre>', title_pos)
if pre_start == -1:
    print("Could not find <pre> tag")
    exit(1)

# Find where this terminal ends (look for the closing tags after lots of content)
# The terminal should end with </pre></div></div>
# We need to find where the log content ends
# Look for the closing </html> tag which is at the end of the raw logs
html_end = content.find('</html>', pre_start)

if html_end == -1:
    print("Could not find </html> marker in log content")
    # The logs might just end before the footer
    # Find the footer
    footer_pos = content.find('<!-- Footer -->', pre_start)
    if footer_pos == -1:
        print("Could not find footer")
        exit(1)
    # The logs end just before the footer
    # Back up to find </pre></div></div>
    search_start = max(0, footer_pos - 200)
    pre_end = content.rfind('</pre>', search_start, footer_pos)
    if pre_end == -1:
        print("Could not find </pre> before footer")
        exit(1)
else:
    # The raw content is after </html> tag
    # Find the </pre> that closes this content
    pre_end = content.find('</pre>', html_end)

if pre_end == -1:
    print("Could not find closing </pre>")
    exit(1)

# Extract the log lines (content between <pre> and </pre>)
log_content = content[pre_start + 5:pre_end]
log_lines = log_content.strip().split('\n')

print(f"Found {len(log_lines)} lines of log content")

# Split into chunks of 100 lines
chunk_size = 100
chunks = []
for i in range(0, len(log_lines), chunk_size):
    chunks.append(log_lines[i:i+chunk_size])

print(f"Creating {len(chunks)} terminal windows")

# Create the section header
section_header = '''
        <!-- System Logs Section -->
        <div class="section-header">
            <i class="bi bi-journal-text"></i>
            <span>System Logs - Detailed Output</span>
        </div>
'''

# Create terminal windows for each chunk
terminals_html = []
for i, chunk in enumerate(chunks, 1):
    terminal = f'''
        <!-- System Logs Part {i} of {len(chunks)} -->
        <div class="terminal-window">
            <div class="terminal-titlebar">
                <div class="terminal-dots">
                    <div class="terminal-dot red"></div>
                    <div class="terminal-dot yellow"></div>
                    <div class="terminal-dot green"></div>
                </div>
                <div class="terminal-title">System Logs - Part {i} of {len(chunks)}</div>
            </div>
            <div class="terminal-body">
                <pre>{'\\n'.join(chunk)}</pre>
            </div>
        </div>
'''
    terminals_html.append(terminal)

# Find where the old terminal div ends (</div></div> after the </pre>)
div_close_1 = content.find('</div>', pre_end)
div_close_2 = content.find('</div>', div_close_1 + 1)

# Replace the old terminal with section header + new terminals
new_content = (
    content[:start_pos] +
    section_header +
    ''.join(terminals_html) +
    content[div_close_2 + 6:]
)

# Write the result
with open('logs and journalctl.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n✓ Successfully created {len(chunks)} terminal windows")
print(f"✓ Added section header")
print(f"✓ Removed old large terminal")
