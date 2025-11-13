#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def generate_version_index(repo_name, version, github_repo):
    """Генерирует index.html для версионной директории"""
    
    versions_dir = f"deploy/{repo_name}"
    current_version_dir = f"{versions_dir}/{version}"
    
    # Получаем список всех версий
    versions = []
    if os.path.exists(versions_dir):
        for item in os.listdir(versions_dir):
            if os.path.isdir(os.path.join(versions_dir, item)) and item != "latest":
                versions.append(item)
    
    # Сортируем версии в обратном порядке (новые версии первыми)
    def version_key(v):
        # Удаляем 'v' и разбиваем на числа
        v_clean = v.lstrip('v')
        parts = v_clean.split('.')
        # Заполняем недостающие части нулями
        while len(parts) < 3:
            parts.append('0')
        return [int(part) for part in parts]
    
    versions.sort(key=version_key, reverse=True)
    
    html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Version {version} - {repo_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background-color: rgba(255, 255, 255, 0.95);
            padding: 2rem 0;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .version-card {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            margin: 1rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .version-list {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            margin: 2rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .version-item {{
            padding: 1rem;
            margin: 0.5rem 0;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #667eea;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .btn {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 0.8rem 1.5rem;
            text-decoration: none;
            border-radius: 5px;
            margin: 0.5rem;
            transition: background 0.3s;
            border: none;
            cursor: pointer;
        }}
        
        .btn:hover {{
            background: #764ba2;
        }}
        
        .btn-small {{
            padding: 0.4rem 0.8rem;
            font-size: 0.9rem;
        }}
        
        .current-version {{
            background: #e8f5e8;
            border-left: 4px solid #4CAF50;
        }}
        
        .version-links {{
            display: flex;
            gap: 0.5rem;
        }}
        
        .language-btn {{
            background: #27ae60;
        }}
        
        .language-btn:hover {{
            background: #219a52;
        }}
        
        .home-btn {{
            background: #e74c3c;
        }}
        
        .home-btn:hover {{
            background: #c0392b;
        }}
        
        .version-info {{
            background: #f39c12;
            color: white;
            padding: 0.5rem;
            border-radius: 3px;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 {repo_name}</h1>
            <p>Version: <strong>{version}</strong></p>
            <div class="version-info">
                Commit: {os.environ.get('GITHUB_SHA', 'Unknown')[:7]}
            </div>
        </header>
        
        <div class="version-card current-version">
            <h2>📦 Current Version: {version}</h2>
            <p>This is version <strong>{version}</strong> of the application deployed from GitHub Actions.</p>
            
            <div style="margin-top: 1rem;">
                <a href="index.html" class="btn">🌐 Open Main Page</a>
                <a href="ru/index.html" class="btn language-btn">🇷🇺 Russian Version</a>
                <a href="en/index.html" class="btn language-btn">🇺🇸 English Version</a>
            </div>
        </div>
        
        <div class="version-list">
            <h2>📚 All Available Versions</h2>
            <p>Select a version to view. Older versions are preserved for reference.</p>
            
            <div class="version-item current-version">
                <div>
                    <strong>{version}</strong> (current)
                    <div style="font-size: 0.9rem; color: #666; margin-top: 0.2rem;">
                        Deployed: {os.environ.get('GITHUB_SHA', 'Unknown')[:7]}
                    </div>
                </div>
                <div class="version-links">
                    <a href="index.html" class="btn btn-small">Main</a>
                    <a href="ru/index.html" class="btn btn-small">RU</a>
                    <a href="en/index.html" class="btn btn-small">EN</a>
                </div>
            </div>
    '''
    
    # Добавляем другие версии
    for ver in versions:
        if ver != version:
            html_content += f'''
            <div class="version-item">
                <div>
                    <strong>{ver}</strong>
                </div>
                <div class="version-links">
                    <a href="../{ver}/index.html" class="btn btn-small">Main</a>
                    <a href="../{ver}/ru/index.html" class="btn btn-small">RU</a>
                    <a href="../{ver}/en/index.html" class="btn btn-small">EN</a>
                </div>
            </div>
            '''
    
    html_content += f'''
        </div>
        
        <div class="version-card">
            <h2>🔗 Quick Links</h2>
            <div>
                <a href="/{repo_name}/latest/index.html" class="btn">📱 Latest Version</a>
                <a href="/{repo_name}/" class="btn home-btn">🏠 Home</a>
                <a href="https://github.com/{github_repo}" class="btn">💻 GitHub Repository</a>
                <a href="https://github.com/{github_repo}/releases" class="btn">🎯 All Releases</a>
            </div>
        </div>
    </div>
</body>
</html>
    '''
    
    # Создаем index.html в директории версии
    index_path = Path(current_version_dir) / "index.html"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated version index for {version}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python generate_html.py <repo_name> <version> <github_repo>")
        sys.exit(1)
    
    repo_name = sys.argv[1]
    version = sys.argv[2]
    github_repo = sys.argv[3]
    
    generate_version_index(repo_name, version, github_repo)
