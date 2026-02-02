#!/usr/bin/env python3
"""
Split the large terminal window in 'logs and journalctl.html' into multiple smaller terminal windows
"""

# Read the original file
with open("logs and journalctl.html", "r") as f:
    lines = f.readlines()

# Find where the System Logs terminal starts and ends  
start_idx = None
end_idx = None

for i, line in enumerate(lines):
    if "System Logs - Detailed Output" in line:
        # Terminal title is at line i, content starts a few lines later
        start_idx = i - 5  # Go back to the start of <div class="terminal-window">
        print(f"Found terminal title at line {i+1}")
    if start_idx is not None and "</pre>" in line and i > start_idx + 15:
        end_idx = i
        print(f"Found closing </pre> at line {i+1}")
        break

if start_idx is None or end_idx is None:
    print(f"Could not find the terminal window! start={start_idx}, end={end_idx}")
    exit(1)

print(f"Terminal title at line: {start_idx + 1}")
print(f"Terminal closes at line: {end_idx + 1}")

# Extract the content lines (between <pre> and </pre>)
content_start = start_idx + 9  # After the titlebar div structure + <pre>
content_lines = lines[content_start:end_idx]

print(f"Total content lines: {len(content_lines)}")

# Split into chunks of 100 lines
chunk_size = 100
num_chunks = (len(content_lines) + chunk_size - 1) // chunk_size

print(f"Will create {num_chunks} terminal windows")

# Generate the new terminal windows
new_terminals = []
for chunk_num in range(num_chunks):
    start = chunk_num * chunk_size
    end = min((chunk_num + 1) * chunk_size, len(content_lines))
    chunk_content = lines[content_start + start:content_start + end]
    
    terminal_html = f'''
        <!-- System Logs Part {chunk_num + 1} -->
        <div class="terminal-window">
            <div class="terminal-titlebar">
                <div class="terminal-dots">
                    <div class="terminal-dot red"></div>
                    <div class="terminal-dot yellow"></div>
                    <div class="terminal-dot green"></div>
                </div>
                <div class="terminal-title">System Logs - Part {chunk_num + 1} of {num_chunks}</div>
            </div>
            <div class="terminal-body">
                <pre>{''.join(chunk_content)}</pre>
            </div>
        </div>
'''
    new_terminals.append(terminal_html)

# Now replace the large terminal with multiple smaller ones
# Everything before the old terminal
output_lines = lines[:start_idx]

# Add all the new terminals
for terminal in new_terminals:
    output_lines.append(terminal)

# Everything after the old terminal
output_lines.extend(lines[end_idx + 4:])  # Skip the closing </div></div></div>

# Write the new file
with open("logs and journalctl.html", "w") as f:
    f.writelines(output_lines)

print(f"✓ Successfully split into {num_chunks} terminal windows!")
print(f"✓ File updated: logs and journalctl.html")
