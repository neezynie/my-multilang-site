#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def add_version_info(directory, version):
    """Добавляет информацию о версии в HTML файлы"""
    
    html_files = list(Path(directory).glob('**/*.html'))
    
    version_banner = f'''
    <div class="version-info">
        <strong>Version:</strong> {version} | 
        <strong>Deployment:</strong> {os.environ.get('GITHUB_SHA', 'Unknown')[:7]}
    </div>
    '''
    
    for html_file in html_files:
        print(f"Processing: {html_file}")
        
        with open(html_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Добавляем баннер версии после открывающего тега body
        if '<body>' in content:
            content = content.replace('<body>', f'<body>\n{version_banner}')
        elif '<body ' in content:
            # Если у body есть атрибуты
            import re
            content = re.sub(r'(<body[^>]*>)', r'\1' + version_banner, content)
        
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python add_version_info.py <directory> <version>")
        sys.exit(1)
    
    directory = sys.argv[1]
    version = sys.argv[2]
    
    add_version_info(directory, version)
    print(f"Version info added to HTML files in {directory}")