#!/usr/bin/env python3
# Read current file
with open("logs and journalctl.html", "r") as f:
    lines = f.readlines()

# Find the old terminal "System Logs - Detailed Output"
old_start = None
old_end = None

for i, line in enumerate(lines):
    if "System Logs - Detailed Output" in line and old_start is None:
        old_start = i - 5  # Go back to <div class="terminal-window">
        print(f"Old terminal starts at line {i+1} (backing up to {old_start+1})")
    if old_start is not None and old_end is None:
        if "gopala@gopala-VMware20-1:~$</pre>" in line:
            old_end = i + 3  # Include closing tags
            print(f"Old terminal ends at line {i+1} (forward to {old_end+1})")
            break

if old_start is not None and old_end is not None:
    # Remove the old terminal
    new_lines = lines[:old_start] + lines[old_end+1:]
    
    with open("logs and journalctl.html", "w") as f:
        f.writelines(new_lines)
    
    print(f"✓ Removed old terminal (lines {old_start+1} to {old_end+1})")
    print(f"✓ New file has {len(new_lines)} lines")
else:
    print("Could not find old terminal to remove")
