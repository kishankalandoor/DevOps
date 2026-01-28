#!/usr/bin/env python3
"""Remove the 'System Logs - Detailed Output' wrapper terminal and add section header."""

with open('logs and journalctl.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the wrapper terminal that contains "System Logs - Detailed Output"
wrapper_start = None
wrapper_title_line = None
wrapper_pre_line = None

for i, line in enumerate(lines):
    if 'System Logs - Detailed Output' in line:
        wrapper_title_line = i
        # Find the start of this terminal window (go backwards)
        for j in range(i, max(0, i-20), -1):
            if '<!-- Additional System Logs Terminal -->' in lines[j]:
                wrapper_start = j
                break
            elif '<div class="terminal-window">' in lines[j] and j < i:
                wrapper_start = j - 1 if j > 0 and '<!--' in lines[j-1] else j
                break
        # Find where the <pre> tag opens
        for j in range(i, min(i+10, len(lines))):
            if '<pre>' in lines[j]:
                wrapper_pre_line = j
                break
        break

if wrapper_start is not None and wrapper_pre_line is not None:
    print(f"Found wrapper terminal:")
    print(f"  Comment/Start: line {wrapper_start + 1}")
    print(f"  Title line: {wrapper_title_line + 1}")
    print(f"  PRE opens: line {wrapper_pre_line + 1}")
    
    # The wrapper structure is:
    # - Comment line (wrapper_start)
    # - <div class="terminal-window">
    # - <div class="terminal-titlebar">
    # - dots
    # - title
    # - </div>
    # - <div class="terminal-body">
    # - <pre>
    #
    # We need to remove from wrapper_start to wrapper_pre_line (inclusive)
    # and add a section header instead
    
    # Create the new section header
    section_header = '''        <!-- System Logs Section -->
        <div class="section-header">
            <i class="bi bi-journal-text"></i>
            <span>System Logs - Detailed Output</span>
        </div>

'''
    
    # Remove the wrapper opening (from start to and including <pre> line)
    new_lines = lines[:wrapper_start] + [section_header] + lines[wrapper_pre_line + 1:]
    
    # Now we need to find and remove the closing </pre></div></div> of the wrapper
    # This should be AFTER all the "Part X of 15" terminals
    # Look for the last "Part 15 of 15" terminal
    last_part_15_line = None
    for i, line in enumerate(new_lines):
        if 'Part 15 of 15' in line:
            last_part_15_line = i
    
    if last_part_15_line:
        # Find the closing of Part 15 terminal
        for i in range(last_part_15_line, min(last_part_15_line + 200, len(new_lines))):
            if '</pre>' in new_lines[i]:
                # Check if next lines are </div></div> (closing the Part 15 terminal)
                if i + 2 < len(new_lines):
                    if '</div>' in new_lines[i+1] and '</div>' in new_lines[i+2]:
                        # After Part 15 closes, there might be the wrapper's closing tags
                        # Check if there are extra </div></div> after this
                        check_line = i + 3
                        if check_line < len(new_lines) and '</pre>' in new_lines[check_line]:
                            print(f"Found wrapper closing </pre> at line {check_line + 1}")
                            # Remove this </pre> and the two </div> after it
                            if check_line + 2 < len(new_lines):
                                new_lines = new_lines[:check_line] + new_lines[check_line + 3:]
                                print("Removed wrapper closing tags")
                        break
    
    # Write the result
    with open('logs and journalctl.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"\n✓ Successfully removed wrapper terminal")
    print(f"✓ Added section header for 'System Logs - Detailed Output'")
    print(f"✓ The 15 split terminals are now independent")
else:
    print("Could not find the wrapper terminal")
