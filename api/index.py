#!/usr/bin/env python3
"""
Vercel API route for Spider-Run Game File Server
"""

import os
import sys
import zipfile
import tempfile
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# HTML template for the download page
DOWNLOAD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spider-Run Game Downloads</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: #000;
            color: #00bfff;
            margin: 0;
            padding: 20px;
            text-align: center;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(0, 191, 255, 0.1);
            border: 2px solid #00bfff;
            border-radius: 10px;
            padding: 30px;
        }
        h1 {
            color: #ff0000;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
            margin-bottom: 30px;
        }
        .download-section {
            margin: 20px 0;
            padding: 20px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 5px;
        }
        .download-btn {
            display: inline-block;
            background: #ff0000;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            margin: 10px;
            font-weight: bold;
            transition: background 0.3s;
        }
        .download-btn:hover {
            background: #cc0000;
        }
        .file-info {
            color: #ffffff;
            font-size: 14px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🕷️ Spider-Run Game Downloads 🕷️</h1>
        
        <div class="download-section">
            <h2>🎮 Game Files</h2>
            <a href="/api/download/game" class="download-btn">Download Complete Game</a>
            <div class="file-info">Includes all game files, assets, and documentation</div>
        </div>
        
        <div class="download-section">
            <h2>📁 Individual Components</h2>
            <a href="/api/download/static" class="download-btn">Download Assets Only</a>
            <div class="file-info">Game images, sounds, and media files</div>
            
            <a href="/api/download/source" class="download-btn">Download Source Code</a>
            <div class="file-info">Python source code and configuration files</div>
        </div>
        
        <div class="download-section">
            <h2>📖 Documentation</h2>
            <a href="/api/download/docs" class="download-btn">Download Documentation</a>
            <div class="file-info">Game design documents and guides</div>
        </div>
        
        <div class="download-section">
            <h2>🎯 Quick Start</h2>
            <p style="color: #ffffff;">
                1. Download the complete game<br>
                2. Extract the ZIP file<br>
                3. Run: <code>python run.py</code><br>
                4. Open: <code>http://localhost:8081</code>
            </p>
        </div>
    </div>
</body>
</html>
"""

def create_zip_file(files_to_include, zip_name):
    """Create a ZIP file with the specified files"""
    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp_file:
        with zipfile.ZipFile(tmp_file.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add static directory
            if os.path.exists('static'):
                for root, dirs, files in os.walk('static'):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, '.')
                        zipf.write(file_path, arcname)
            
            # Add other files
            for file in files_to_include:
                if os.path.exists(file):
                    zipf.write(file, file)
        
        # Read the ZIP file content
        with open(tmp_file.name, 'rb') as f:
            content = f.read()
        
        # Clean up temporary file
        os.unlink(tmp_file.name)
        
        return content

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == '/' or path == '/index.html':
            # Serve the download page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(DOWNLOAD_HTML.encode())
            
        elif path == '/api/download/game':
            # Download complete game
            files_to_include = [
                'run.py', 'app.py', 'requirements.txt', 'runtime.txt',
                'vercel.json', '.vercelignore', 'DEPLOYMENT.md'
            ]
            zip_content = create_zip_file(files_to_include, 'spider-run-game.zip')
            
            self.send_response(200)
            self.send_header('Content-type', 'application/zip')
            self.send_header('Content-Disposition', 'attachment; filename="spider-run-game.zip"')
            self.end_headers()
            self.wfile.write(zip_content)
            
        elif path == '/api/download/static':
            # Download static assets only
            zip_content = create_zip_file([], 'spider-run-assets.zip')
            
            self.send_response(200)
            self.send_header('Content-type', 'application/zip')
            self.send_header('Content-Disposition', 'attachment; filename="spider-run-assets.zip"')
            self.end_headers()
            self.wfile.write(zip_content)
            
        elif path == '/api/download/source':
            # Download source code only
            files_to_include = [
                'run.py', 'app.py', 'requirements.txt', 'runtime.txt',
                'vercel.json', '.vercelignore', 'DEPLOYMENT.md'
            ]
            zip_content = create_zip_file(files_to_include, 'spider-run-source.zip')
            
            self.send_response(200)
            self.send_header('Content-type', 'application/zip')
            self.send_header('Content-Disposition', 'attachment; filename="spider-run-source.zip"')
            self.end_headers()
            self.wfile.write(zip_content)
            
        elif path == '/api/download/docs':
            # Download documentation
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp_file:
                with zipfile.ZipFile(tmp_file.name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    if os.path.exists('Docs'):
                        for root, dirs, files in os.walk('Docs'):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.relpath(file_path, '.')
                                zipf.write(file_path, arcname)
                    
                    # Add README and deployment guide
                    if os.path.exists('README.md'):
                        zipf.write('README.md', 'README.md')
                    if os.path.exists('DEPLOYMENT.md'):
                        zipf.write('DEPLOYMENT.md', 'DEPLOYMENT.md')
                
                # Read the ZIP file content
                with open(tmp_file.name, 'rb') as f:
                    content = f.read()
                
                # Clean up temporary file
                os.unlink(tmp_file.name)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/zip')
            self.send_header('Content-Disposition', 'attachment; filename="spider-run-docs.zip"')
            self.end_headers()
            self.wfile.write(content)
            
        else:
            # 404 for unknown paths
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')
