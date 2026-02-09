#!/usr/bin/env python3
"""
Rebuild bash activities.html with:
- Content divided into multiple terminal windows
- Black background with white text in terminals
- Bootstrap light theme for page
- No emojis
"""

import html
import re

def extract_terminal_content(filename):
    """Extract raw terminal content"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    start_marker = "Last login: Tue Feb  3 15:06:40"
    end_marker = "[Message clipped]"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        # Extract content up to but NOT including "[Message clipped]"
        return content[start_idx:end_idx].strip()
    return ""

def divide_into_sections(terminal_content):
    """Divide terminal content into logical sections"""
    lines = terminal_content.split('\n')
    
    sections = []
    current_lines = []
    current_title = "Bash Scripting and Environment Setup"
    
    i = 0
    while i < len(lines):
        line = lines[i]
        current_lines.append(line)
        
        # Create new section every ~150 lines or at major topic changes
        if len(current_lines) >= 150:
            # Look for a good break point
            if ('cd /Applications' in line or 
                'grep' in line and i > 100 or
                'nmap' in line or
                'host' in line and 'pacewisdom' in line or
                'docker' in line or
                'nginx' in line or
                'sed' in line and i > 200 or
                'awk' in line and i > 300 or
                'cut' in line and i > 400 or
                'env' in line and i > 500 or
                'wc' in line and i > 600):
                
                # Determine title based on content
                content_str = '\n'.join(current_lines[-20:]).lower()
                
                if 'grep' in content_str and 'text' not in current_title.lower():
                    new_title = "Grep and Pattern Matching"
                elif 'nmap' in content_str or 'host' in content_str or 'dig' in content_str:
                    new_title = "Network Tools - Nmap, Host, Dig"
                elif 'docker' in content_str or 'nginx' in content_str:
                    new_title = "Docker and Nginx Configuration"
                elif 'sed' in content_str:
                    new_title = "Sed - Stream Editor"
                elif 'awk' in content_str:
                    new_title = "AWK Text Processing"
                elif 'cut' in content_str:
                    new_title = "Cut and Text Manipulation"
                elif 'env' in content_str or 'export' in content_str:
                    new_title = "Environment Variables"
                elif 'sort' in content_str or 'uniq' in content_str:
                    new_title = "Sort, Uniq, and Data Processing"
                elif 'wc' in content_str:
                    new_title = "Word Count and File Statistics"
                else:
                    new_title = current_title
                
                sections.append((current_title, '\n'.join(current_lines)))
                current_lines = []
                current_title = new_title
        
        i += 1
    
    # Add remaining lines
    if current_lines:
        sections.append((current_title, '\n'.join(current_lines)))
    
    return sections

def create_html(sections):
    """Create full HTML with multiple terminal windows"""
    
    terminal_windows = ""
    for i, (title, content) in enumerate(sections):
        # Escape HTML special characters for proper display
        escaped_content = html.escape(content)
        terminal_windows += f'''
        <h2 class="section-header">Terminal Session {i+1}: {title}</h2>

        <div class="terminal-window">
            <div class="terminal-header">
                <div class="terminal-controls">
                    <span class="terminal-dot red"></span>
                    <span class="terminal-dot yellow"></span>
                    <span class="terminal-dot green"></span>
                </div>
                <div class="terminal-title">{title}</div>
            </div>
            <div class="terminal-body">
                <pre>{escaped_content}</pre>
            </div>
        </div>
'''
    
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bash Activities - Terminal History</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            background: #f5f5f7;
            color: #1d1d1f;
            line-height: 1.6;
        }}

        .page-header {{
            background: #ffffff;
            color: #1d1d1f;
            padding: 60px 40px;
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 1px solid #d2d2d7;
        }}

        .page-header h1 {{
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 10px;
        }}

        .page-header .subtitle {{
            font-size: 18px;
            color: #6e6e73;
        }}

        .section-header {{
            color: #1d1d1f;
            font-size: 28px;
            font-weight: 700;
            margin: 50px 0 25px 0;
            padding: 15px 20px;
            background: #ffffff;
            border-left: 4px solid #0071e3;
            border-radius: 6px;
        }}

        .terminal-window {{
            background: #2d2d2d;
            border-radius: 8px;
            border: 1px solid #404040;
            margin-bottom: 25px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }}

        .terminal-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 20px;
            background: #1e1e1e;
            border-bottom: 1px solid #404040;
        }}

        .terminal-controls {{
            display: flex;
            gap: 8px;
        }}

        .terminal-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }}

        .terminal-dot.red {{
            background: #ff5f56;
        }}

        .terminal-dot.yellow {{
            background: #ffbd2e;
        }}

        .terminal-dot.green {{
            background: #27c93f;
        }}

        .terminal-title {{
            flex: 1;
            text-align: center;
            color: #d4d4d4;
            font-size: 13px;
            font-weight: 600;
            margin-right: 40px;
        }}

        .terminal-body {{
            padding: 20px;
            font-family: 'SF Mono', Monaco, 'Courier New', monospace;
            font-size: 13px;
            color: #00ff00;
            background: #000000;
            max-height: 500px;
            overflow-y: auto;
            overflow-x: auto;
        }}

        .terminal-body pre {{
            margin: 0;
            white-space: pre-wrap;
            line-height: 1.5;
            color: #00ff00;
        }}

        .terminal-body::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}

        .terminal-body::-webkit-scrollbar-track {{
            background: #1a1a1a;
        }}

        .terminal-body::-webkit-scrollbar-thumb {{
            background: #404040;
            border-radius: 5px;
        }}

        .terminal-body::-webkit-scrollbar-thumb:hover {{
            background: #555555;
        }}

        .scroll-top {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background: #0071e3;
            color: #ffffff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 113, 227, 0.3);
            transition: all 0.3s ease;
            opacity: 0;
            visibility: hidden;
            z-index: 1000;
        }}

        .scroll-top.visible {{
            opacity: 1;
            visibility: visible;
        }}

        .scroll-top:hover {{
            transform: translateY(-5px);
            box-shadow: 0 6px 16px rgba(0, 113, 227, 0.5);
        }}
    </style>
</head>

<body>
    <div class="page-header">
        <h1>Bash Activities Terminal History</h1>
        <p class="subtitle">Complete DevOps Terminal Sessions - Divided by Topic</p>
    </div>

    <div class="container">
{terminal_windows}
    </div>

    <div class="scroll-top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">
        ↑
    </div>

    <footer class="bg-light text-center py-4 mt-5">
        <p class="mb-0 text-muted">&copy; 2026 DevOps Terminal Documentation</p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.js"></script>
    <script>
        window.addEventListener('scroll', function() {{
            const scrollTop = document.querySelector('.scroll-top');
            if (window.pageYOffset > 300) {{
                scrollTop.classList.add('visible');
            }} else {{
                scrollTop.classList.remove('visible');
            }}
        }});
    </script>
</body>
</html>'''
    
    return html_template

def main():
    print("Extracting terminal content...")
    terminal_content = extract_terminal_content('bash_history_backup.html')
    
    if not terminal_content:
        print("ERROR: Could not extract terminal content!")
        return
    
    print(f"Extracted {len(terminal_content)} characters")
    
    print("\nDividing into sections...")
    sections = divide_into_sections(terminal_content)
    
    print(f"Created {len(sections)} terminal windows:")
    for i, (title, content) in enumerate(sections):
        print(f"  {i+1}. {title}: {len(content.split(chr(10)))} lines")
    
    print("\nGenerating HTML...")
    html_content = create_html(sections)
    
    print("Writing to 'bash activities.html'...")
    with open('bash activities.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\nDone! Created {len(sections)} terminal windows")
    print(f"Total file size: {len(html_content):,} bytes")

if __name__ == "__main__":
    main()
