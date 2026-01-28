#!/usr/bin/env python3
"""
Rebuild the logs and journalctl.html file with properly split terminal windows
"""

# Read the backup file
with open("logs and journalctl_backup_original.html", "r") as f:
    content = f.read()

# Find where the HTML ends and raw content begins
html_end = content.find("</html>")
if html_end == -1:
    print("Error: Could not find </html> tag")
    exit(1)

# Split into HTML part and raw logs part
html_part = content[:html_end + 7]  # Include </html>
raw_logs = content[html_end + 8:].strip()  # Everything after </html>

if not raw_logs:
    print("No raw logs found after </html>")
    exit(1)

print(f"Found {len(raw_logs.split(chr(10)))} lines of raw logs")

# Split raw logs into lines
log_lines = raw_logs.split('\n')
total_lines = len(log_lines)
print(f"Total log lines: {total_lines}")

# Create chunks of 100 lines each
chunk_size = 100
chunks = []
for i in range(0, total_lines, chunk_size):
    chunk = log_lines[i:i+chunk_size]
    chunks.append(chunk)

num_chunks = len(chunks)
print(f"Creating {num_chunks} terminal windows")

# Find where to insert the new terminals (before the footer)
footer_pos = html_part.find('<!-- Footer -->')
if footer_pos == -1:
    print("Error: Could not find footer")
    exit(1)

# Build the new terminals HTML
terminals_html = ""
for idx, chunk in enumerate(chunks):
    chunk_text = '\n'.join(chunk)
    terminals_html += f'''
        <!-- System Logs Part {idx + 1} of {num_chunks} -->
        <div class="terminal-window">
            <div class="terminal-titlebar">
                <div class="terminal-dots">
                    <div class="terminal-dot red"></div>
                    <div class="terminal-dot yellow"></div>
                    <div class="terminal-dot green"></div>
                </div>
                <div class="terminal-title">System Logs - Part {idx + 1} of {num_chunks}</div>
            </div>
            <div class="terminal-body">
                <pre>{chunk_text}</pre>
            </div>
        </div>

'''

# Insert the terminals before the footer
new_html = html_part[:footer_pos] + terminals_html + html_part[footer_pos:]

# Write the new file
with open("logs and journalctl.html", "w") as f:
    f.write(new_html)

print(f"✓ Successfully created {num_chunks} terminal windows!")
print(f"✓ File saved: logs and journalctl.html")
