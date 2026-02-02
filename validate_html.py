
import re

def validate_html(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    stack = []
    
    print("Tracing main blocks (Level 0 = main-container?):")

    for i, line in enumerate(lines):
        line = line.strip()
        starts = [m.start() for m in re.finditer(r'<div\b', line)]
        ends = [m.start() for m in re.finditer(r'</div>', line)]
        
        # Simple stack simulation
        # Note: multiple tags on one line handled by iterating through chars is better, 
        # but here we assume no mix of start/end on same line for major blocks.
        
        diff = len(starts) - len(ends)
        
        if diff > 0:
            for _ in range(diff):
                stack.append(i + 1)
                if len(stack) <= 2:
                    print(f"Level {len(stack)} Open at {i+1}")
        elif diff < 0:
            for _ in range(abs(diff)):
                if len(stack) <= 2:
                    print(f"Level {len(stack)} Close at {i+1}")
                if stack:
                    stack.pop()
                else:
                    print(f"Error: Extra closing div at {i+1}")

    if stack:
        print(f"Unclosed divs: {len(stack)}")
    
validate_html('/Applications/XAMPP/xamppfiles/htdocs/DevOps/nginx.html')
