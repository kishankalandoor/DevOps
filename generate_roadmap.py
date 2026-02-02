import pandas as pd
import html
import re
import os
import datetime
from pathlib import Path

def make_clickable(text):
    text = str(text)
    url_pattern = re.compile(r'(https?://\S+)')
    
    parts = text.split()
    new_parts = []
    for part in parts:
        if part.startswith('http://') or part.startswith('https://'):
            link = f'<a href="{part}" target="_blank">{part}</a>'
            new_parts.append(link)
        else:
            new_parts.append(html.escape(part))
    return " ".join(new_parts)

def get_file_info(directory):
    files_data = []
    # extensions to look for
    valid_exts = {'.html', '.txt'}
    
    for filename in os.listdir(directory):
        if filename == 'roadmap.html': continue # Skip self
        
        ext = os.path.splitext(filename)[1].lower()
        if ext in valid_exts:
            filepath = os.path.join(directory, filename)
            stats = os.stat(filepath)
            
            # map ext to display type and icon
            file_type = 'html' if ext == '.html' else 'txt'
            icon = 'bi-filetype-html' if ext == '.html' else 'bi-file-text'
            if ext == '.html':
                 # Custom icons based on name (heuristic)
                 lower_name = filename.lower()
                 if 'password' in lower_name: icon = 'bi-shield-lock'
                 elif 'inode' in lower_name: icon = 'bi-hdd'
                 elif 'nmap' in lower_name: icon = 'bi-radar'
                 elif 'nginx' in lower_name: icon = 'bi-globe'
                 elif 'log' in lower_name: icon = 'bi-journal-text'
                 elif 'date' in lower_name: icon = 'bi-calendar-check'
                 elif 'dig' in lower_name: icon = 'bi-search'
                 elif 'netstat' in lower_name: icon = 'bi-diagram-3'
                 elif 'ping' in lower_name: icon = 'bi-arrow-repeat'
            
            # Creation time (using st_mtime as proxy for modification/creation on some systems)
            # On Mac st_birthtime exists
            try:
                date_ts = stats.st_birthtime
            except AttributeError:
                date_ts = stats.st_mtime
                
            date_str = datetime.datetime.fromtimestamp(date_ts).strftime('%b %d %Y')
            
            files_data.append({
                'name': filename,
                'type': file_type,
                'icon': icon,
                'date': date_ts, # keep timestamp for sorting
                'date_display': date_str,
                'topic': filename.replace('.html', '').replace('.txt', '').replace('-', ' ').title()
            })
            
    # Sort by date descending
    files_data.sort(key=lambda x: x['date'], reverse=True)
    return files_data

try:
    # 1. Read Excel for Roadmap
    df = pd.read_excel('devops.xlsx')
    df.columns = df.columns.str.strip()
    df = df.fillna('')
    
    tasks = []
    current_task = None
    
    for index, row in df.iterrows():
        task_text = str(row.get('Tasks', '')).strip()
        material = str(row.get('Training Material', '')).strip()
        status = str(row.get('Status', '')).strip()
        date_raw = row.get('Date', '')
        
        date_str = str(date_raw)
        if hasattr(date_raw, 'strftime'):
             date_str = date_raw.strftime('%Y-%m-%d')
        elif isinstance(date_raw, (int, float)) and date_raw > 1000000000:
             try:
                 dt = pd.to_datetime(date_raw, unit='ms')
                 date_str = dt.strftime('%Y-%m-%d')
             except:
                 pass

        if task_text:
            current_task = {
                'title': task_text,
                'resources': [],
                'status': status,
                'date': date_str if date_str != 'nan' and date_str else ''
            }
            if material:
                current_task['resources'].append(material)
            tasks.append(current_task)
        elif current_task and material:
            current_task['resources'].append(material)

    # 2. Scan Directory for Dashboard
    repo_files = get_file_info('.')
    html_files = [f for f in repo_files if f['type'] == 'html']
    txt_files = [f for f in repo_files if f['type'] == 'txt']

    # 3. Match Files to Tasks (Integration)
    # Heuristic: Check if important words from filename exist in task title
    # or if task title words exist in filename
    
    unmatched_files = list(repo_files) # Copy to track what's left
    
    for task in tasks:
        task['linked_file'] = None
        task_title_lower = task['title'].lower()
        
        # Strategy 1: exact keyword matching
        # We look for the file that best matches this task
        best_match = None
        best_score = 0
        
        for file in repo_files:
            # clean filename for matching
            fname_base = file['name'].lower().replace('.html', '').replace('.txt', '').replace('-', ' ').replace('_', ' ')
            
            # Check overlap
            # 1. Filename is contained in Task Title (e.g. "nginx" in "Explore Nginx")
            if fname_base in task_title_lower and len(fname_base) > 3:
                score = len(fname_base)
                if score > best_score:
                    best_score = score
                    best_match = file
            
            # 2. Task Title contained in Filename (less likely but possible)
            # e.g. "inode" in "inode.html"
            # Split task into words
            task_words = [w for w in task_title_lower.split() if len(w) > 3]
            match_count = sum(1 for w in task_words if w in fname_base)
            if match_count > 0:
                score = match_count * 10 # Weight words higher
                if score > best_score:
                    best_score = score
                    best_match = file

        if best_match:
            task['linked_file'] = best_match
            # If we haven't manually set status, and we have a file, assume it's done-ish?
            # User might prefer explicit status, but let's at least flag it
            if not task['status']:
                task['status'] = 'Submitted'
            
            # Remove from unmatched files for the top list? 
            # User might want to see ALL files at top, OR only unlinked ones.
            # "Integrate ... to respective roadmap" suggests moving them.
            # But let's keep the Dashboard as a full index for now, just to be safe.
            pass

    # 4. Generate HTML
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Digital Report & Roadmap</title>
    <!-- Using CDN for Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    
    <style>
        :root {
            --bg-body: #f5f5f7;
            --bg-card: #ffffff;
            --text-primary: #1d1d1f;
            --text-secondary: #86868b;
            --border-color: #e0e0e0;
            --accent: #0071e3;
            --success: #34c759;
            --warning: #ff9500;
            --card-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            --hover-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: var(--bg-body);
            color: var(--text-primary);
            margin: 0;
            padding: 40px 20px;
            line-height: 1.47059;
            font-weight: 400;
            -webkit-font-smoothing: antialiased;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            margin-bottom: 60px;
            background: var(--bg-card);
            padding: 60px 40px;
            border-radius: 24px;
            box-shadow: var(--card-shadow);
        }
        
        h1 {
            font-size: 48px;
            line-height: 1.08;
            font-weight: 700;
            letter-spacing: -0.003em;
            margin: 0 0 10px 0;
            color: var(--text-primary);
        }
        
        p.subtitle {
            font-size: 24px;
            line-height: 1.33;
            font-weight: 400;
            color: var(--text-secondary);
        }
        
        .intern-name {
            font-size: 20px;
            font-weight: 600;
            margin-top: 20px;
            color: var(--text-primary);
        }

        /* Stats Grid */
        .stats-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 60px;
        }

        .stat-card {
            background: var(--bg-card);
            border-radius: 18px;
            padding: 30px;
            text-align: center;
            box-shadow: var(--card-shadow);
            border: 1px solid var(--border-color);
        }

        .stat-number {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #1d1d1f 0%, #434344 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .stat-label {
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
        }

        .section-title {
            font-size: 32px;
            font-weight: 700;
            margin: 60px 0 30px;
            color: var(--text-primary);
            padding-bottom: 15px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            gap: 15px;
        }

        /* Roadmap Timeline */
        .timeline {
            position: relative;
            padding-left: 50px;
            margin-top: 40px;
        }
        
        .timeline::before {
            content: '';
            position: absolute;
            left: 15px;
            top: 20px;
            bottom: 0;
            width: 2px;
            background-color: var(--border-color);
        }

        .task-card {
            background-color: var(--bg-card);
            border-radius: 18px;
            padding: 30px;
            margin-bottom: 40px;
            box-shadow: var(--card-shadow);
            transition: all 0.3s ease;
            position: relative;
            border: 1px solid var(--border-color);
        }
        
        .task-card:hover {
            transform: scale(1.01);
            box-shadow: var(--hover-shadow);
            border-color: var(--text-primary);
        }
        
        /* Different styling for connected tasks to highlight integration */
        .task-card.has-file {
            border-left: 5px solid var(--accent);
        }
        
        .timeline-dot {
            position: absolute;
            left: -57px;
            top: 35px;
            width: 14px;
            height: 14px;
            background-color: var(--bg-card);
            border: 3px solid var(--text-secondary);
            border-radius: 50%;
            z-index: 10;
        }
        
        .task-card.has-file .timeline-dot {
            border-color: var(--accent);
            background-color: var(--accent);
        }

        .task-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 20px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }

        .task-title {
            font-size: 24px;
            font-weight: 600;
            color: var(--text-primary);
        }

        .status-badge {
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .status-done {
            background-color: #e8f5e9;
            color: #1b5e20;
        }
        
        .status-submitted {
            background-color: #e3f2fd;
            color: #0277bd;
        }
        
        .status-pending {
            background-color: #fff3e0;
            color: #e65100;
        }

        .resources-box {
            background: #fbfbfd;
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
        }

        .resources-box a {
            color: var(--accent);
            text-decoration: none;
        }
        
        .resources-box a:hover {
            text-decoration: underline;
        }
        
        /* Linked File Card inside Task */
        .linked-file {
            display: flex;
            align-items: center;
            gap: 15px;
            background: #f5f5f7;
            padding: 15px;
            border-radius: 12px;
            margin-top: 20px;
            text-decoration: none;
            color: var(--text-primary);
            border: 1px solid transparent;
            transition: all 0.2s;
        }
        
        .linked-file:hover {
            background: #e8e8ed;
            border-color: var(--border-color);
        }
        
        .linked-file-icon {
            font-size: 24px;
            color: var(--text-secondary);
        }
        
        .linked-file-info {
            flex: 1;
        }
        
        .linked-file-name {
            font-weight: 600;
            font-size: 14px;
        }
        
        .linked-file-meta {
            font-size: 12px;
            color: var(--text-secondary);
        }

        footer {
            margin-top: 80px;
            padding: 40px 0;
            text-align: center;
            border-top: 1px solid var(--border-color);
            color: var(--text-secondary);
        }

        @media (max-width: 768px) {
            h1 { font-size: 32px; }
            .timeline { padding-left: 30px; }
            .timeline::before { left: 8px; }
            .timeline-dot { left: -42px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>DevOps Digital Report</h1>
            <p class="subtitle">Trajectory & Repository Dashboard</p>
            <p class="intern-name">Kishan K</p>
        </header>

        <!-- Stats Section -->
        <div class="stats-section">
            <div class="stat-card">
                <div class="stat-number">""" + str(len(html_files)) + """</div>
                <div class="stat-label">HTML Files</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">""" + str(len(txt_files)) + """</div>
                <div class="stat-label">Text Files</div>
            </div>
             <div class="stat-card">
                <div class="stat-number">""" + str(len(tasks)) + """</div>
                <div class="stat-label">Total Tasks</div>
            </div>
        </div>

        <!-- Timeline Section -->
        <h2 class="section-title"><i class="bi bi-signpost-2"></i> Learning Roadmap</h2>
        <div class="timeline">
"""

    # Add Timeline Cards
    for task in tasks:
        status_text = task['status']
        status_class = "status-pending"
        
        if status_text and any(x in status_text.lower() for x in ['done', 'completed', 'verified', 'executed']):
            status_class = "status-done"
        elif status_text and 'submitted' in status_text.lower():
             status_class = "status-submitted"
        elif task['linked_file']: # Auto-generated status
             status_class = "status-submitted"
             if not status_text: status_text = "Completed"
        
        date_display = task["date"]
        linked_file = task['linked_file']
        has_file_class = "has-file" if linked_file else ""
        
        html_content += f"""
            <div class="task-card {has_file_class}">
                <div class="timeline-dot"></div>
                <div class="task-header">
                    <div class="task-title">{html.escape(task['title'])}</div>
                    <div>
                        { f'<span class="status-badge {status_class}">{html.escape(status_text)}</span>' if status_text else '' }
                        { f'<span class="status-badge" style="background:#f5f5f7; color:#666">{html.escape(date_display)}</span>' if date_display else '' }
                    </div>
                </div>
        """
        
        # Linked File Section
        if linked_file:
            html_content += f"""
            <a href="{linked_file['name']}" class="linked-file" target="_blank">
                <div class="linked-file-icon"><i class="bi {linked_file['icon']}"></i></div>
                <div class="linked-file-info">
                     <div class="linked-file-name">View Work: {linked_file['name']}</div>
                     <div class="linked-file-meta">Modified: {linked_file['date_display']}</div>
                </div>
                <div><i class="bi bi-arrow-right-short" style="font-size:20px;"></i></div>
            </a>
            """

        if task['resources']:
            html_content += """<div class="resources-box">"""
            for res in task['resources']:
                html_content += f'<div style="margin-bottom:8px;">{make_clickable(res)}</div>'
            html_content += """</div>"""
        
        html_content += "</div>"

    html_content += """
        </div>

        <footer>
            <p>Generated on """ + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + """</p>
        </footer>
    </div>
</body>
</html>
"""

    with open('roadmap.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Successfully generated merged roadmap.html")

except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

