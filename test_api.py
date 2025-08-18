#!/usr/bin/env python3
"""
Test script for the Vercel API
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from api.index import handler
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import threading
    import requests
    import time
    
    print("✅ Successfully imported API handler")
    
    # Create a simple test server
    class TestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            # Create a mock request
            self.path = self.path
            handler(self)
    
    # Start test server
    server = HTTPServer(('localhost', 8082), TestHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    
    # Wait a moment for server to start
    time.sleep(1)
    
    # Test the API
    try:
        response = requests.get('http://localhost:8082/')
        if response.status_code == 200:
            print("✅ API serves HTML page correctly")
            if "Spider-Run Game Downloads" in response.text:
                print("✅ Correct download page content")
            else:
                print("❌ Wrong page content")
        else:
            print(f"❌ API failed with status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        server.shutdown()
        server.server_close()
    
    print("🎉 API test completed!")
    
except ImportError as e:
    print(f"❌ Failed to import API: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Test failed: {e}")
    sys.exit(1)
