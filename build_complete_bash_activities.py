#!/usr/bin/env python3
"""
Script to rebuild bash activities.html with ALL terminal content
from bash_history_backup.html - Bootstrap light theme, no emojis
"""

import re
import html

def extract_terminal_content(filename):
    """Extract raw terminal content from backup HTML file"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract terminal content
    start_marker = "Last login: Tue Feb  3 15:06:40"
    end_marker = "[Message clipped]"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        terminal_content = content[start_idx:end_idx + len(end_marker)]
        return terminal_content.strip()
    return ""

def create_html_structure(terminal_content):
    """Create full HTML with Bootstrap and all terminal content"""
    
    # Escape HTML special characters in terminal content
    terminal_content_escaped = html.escape(terminal_content)
    
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bash Activities - Complete Terminal History</title>
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
            background: #ffffff;
            border-radius: 8px;
            border: 1px solid #d2d2d7;
            margin-bottom: 25px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}

        .terminal-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 20px;
            background: #f5f5f7;
            border-bottom: 1px solid #d2d2d7;
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
            color: #1d1d1f;
            font-size: 13px;
            font-weight: 600;
            margin-right: 40px;
        }}

        .terminal-body {{
            padding: 20px;
            font-family: 'SF Mono', Monaco, 'Courier New', monospace;
            font-size: 13px;
            color: #1d1d1f;
            background: #fafafa;
            max-height: 600px;
            overflow-y: auto;
            overflow-x: auto;
        }}

        .terminal-body pre {{
            margin: 0;
            white-space: pre-wrap;
            line-height: 1.5;
            color: #1d1d1f;
        }}

        .terminal-body::-webkit-scrollbar {{
            width: 10px;
            height: 10px;
        }}

        .terminal-body::-webkit-scrollbar-track {{
            background: #e5e5e7;
        }}

        .terminal-body::-webkit-scrollbar-thumb {{
            background: #d2d2d7;
            border-radius: 5px;
        }}

        .terminal-body::-webkit-scrollbar-thumb:hover {{
            background: #aeaeb2;
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
        <p class="subtitle">Complete DevOps Terminal Session Documentation - All 1857 Lines</p>
    </div>

    <div class="container">
        <h2 class="section-header">Complete Terminal Session History</h2>

        <div class="terminal-window">
            <div class="terminal-header">
                <div class="terminal-controls">
                    <span class="terminal-dot red"></span>
                    <span class="terminal-dot yellow"></span>
                    <span class="terminal-dot green"></span>
                </div>
                <div class="terminal-title">Full Terminal History - All Commands and Outputs</div>
            </div>
            <div class="terminal-body">
                <pre>{terminal_content_escaped}</pre>
            </div>
        </div>
    </div>

    <div class="scroll-top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">
        ↑
    </div>

    <footer class="bg-light text-center py-4 mt-5">
        <p class="mb-0 text-muted">&copy; 2026 DevOps Terminal Documentation | All Sessions Logged</p>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
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
    print("Extracting terminal content from bash_history_backup.html...")
    terminal_content = extract_terminal_content('bash_history_backup.html')
    
    if not terminal_content:
        print("ERROR: Could not extract terminal content!")
        return
    
    print(f"Extracted {len(terminal_content)} characters of terminal content")
    print(f"Approximately {len(terminal_content.split(chr(10)))} lines")
    
    print("\nGenerating HTML...")
    html_content = create_html_structure(terminal_content)
    
    print("Writing to 'bash activities.html'...")
    with open('bash activities.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("\nDone! File created successfully")
    print(f"Total file size: {len(html_content):,} bytes")

if __name__ == "__main__":
    main()
