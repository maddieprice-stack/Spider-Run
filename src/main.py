"""
Main application module
"""

from flask import Flask, render_template, jsonify, request
import subprocess
import sys
import os
from io import StringIO
import contextlib

app = Flask(__name__)

def run_script():
    """Run the original script logic and capture output"""
    try:
        # Import and run the original main function
        from script_runner import run_original_main
        
        # Capture stdout
        import sys
        from io import StringIO
        
        # Redirect stdout to capture output
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Run the original main function
            result = run_original_main()
            captured_output = sys.stdout.getvalue()
            
            return {
                'success': True,
                'stdout': captured_output + (result if result else ''),
                'stderr': '',
                'return_code': 0
            }
        finally:
            # Restore stdout
            sys.stdout = old_stdout
            
    except Exception as e:
        return {
            'success': False,
            'stdout': '',
            'stderr': str(e),
            'return_code': -1
        }

@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def execute_script():
    """Execute the run.py script and return results"""
    result = run_script()
    return jsonify(result)

def main():
    """Main function to run the Flask application"""
    print("Starting Flask web server...")
    print("Your application will be available at http://localhost:8080")
    app.run(debug=True, host='0.0.0.0', port=8080)

if __name__ == "__main__":
    main()


