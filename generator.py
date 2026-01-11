import os
import sys
import http.server
import socketserver
import webbrowser
import threading
from effects_library import EFFECTS

TEMPLATE_DIR = "."
OUTPUT_DIR = "output"
SKETCH_TEMPLATE = "sketch_base.js"
HTML_TEMPLATE = "index.html"
PORT = 8000

def load_template(filename):
    path = os.path.join(os.path.dirname(__file__), TEMPLATE_DIR, filename)
    with open(path, 'r') as f:
        return f.read()

def write_output(filename, content):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w') as f:
        f.write(content)
    print(f"✓ Generated: {path}")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=OUTPUT_DIR, **kwargs)

    def do_GET(self):
        if self.path == '/shutdown':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Server shutting down...")
            print("\nRemote shutdown requested. Exiting.")
            threading.Timer(0.5, lambda: os._exit(0)).start()
        else:
            super().do_GET()

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def start_server():
    print(f"Serving '{OUTPUT_DIR}/' at http://localhost:{PORT}")
    print("Press Ctrl+C to stop.")
    webbrowser.open(f"http://localhost:{PORT}")
    with ReusableTCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")
            httpd.server_close()

def main():
    print("========================================")
    print("   PixelSynth - Sketch Generator  ")
    print("========================================")
    
    # 1. Menu Selection
    print("\nSelect an effect:")
    for key, effect in EFFECTS.items():
        print(f"[{key}] {effect['name']} - {effect['description']}")
    
    choice = input("\nEnter choice (1-78): ").strip()
    
    if choice not in EFFECTS:
        print("Invalid selection. Exiting.")
        sys.exit(1)
        
    selected_effect = EFFECTS[choice]
    print(f"\nGenerating '{selected_effect['name']}'...")
    
    # 2. Read Templates
    try:
        base_js = load_template(SKETCH_TEMPLATE)
        base_html = load_template(HTML_TEMPLATE)
    except FileNotFoundError as e:
        print(f"Error: Could not find template files. {e}")
        sys.exit(1)

    # 3. Inject Logic
    # Replace placeholders with effect logic
    final_js = base_js.replace("{{GLOBAL_VARS}}", selected_effect["global_vars"])
    final_js = final_js.replace("{{DRAW_LOOP_LOGIC}}", selected_effect["draw_loop"])
    
    # 4. Write Output
    write_output("sketch.js", final_js)
    write_output("index.html", base_html)
    
    print("\nSuccess! Starting server...")
    start_server()

if __name__ == "__main__":
    main()