import webview
import subprocess
import os
import time
import sys
import threading
import signal

# Detect if running as PyInstaller bundle
def get_base_path():
    """Get the base path whether running as script or bundled executable"""
    if getattr(sys, 'frozen', False):
        # Running as bundled exe - use the temp extracted path
        return sys._MEIPASS
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

# Check if this is a subprocess (to avoid infinite recursion in PyInstaller)
def is_subprocess():
    """Check if we're running as a spawned backend subprocess"""
    return os.environ.get('GUITEST_BACKEND') == '1'

backend_process = None

def signal_handler(sig, frame):
    """Handle shutdown gracefully"""
    global backend_process
    if backend_process:
        try:
            backend_process.terminate()
            backend_process.wait(timeout=3)
        except:
            backend_process.kill()
    sys.exit(0)

# Start FastAPI backend server
def start_backend():
    """Start the FastAPI backend server"""
    global backend_process
    
    base_path = get_base_path()
    backend_path = os.path.join(base_path, "backend")
    backend_main = os.path.join(backend_path, "main.py")
    
    # Verify backend exists
    if not os.path.exists(backend_main):
        print(f"ERROR: Backend not found at {backend_main}")
        raise FileNotFoundError(f"Backend not found at {backend_main}")
    
    try:
        # Set environment variable to prevent subprocess from trying to start UI
        env = os.environ.copy()
        env['GUITEST_BACKEND'] = '1'
        
        # Use appropriate flags for Windows
        startupinfo = None
        if sys.platform == 'win32':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
        
        backend_process = subprocess.Popen(
            [sys.executable, backend_main],
            cwd=backend_path,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            startupinfo=startupinfo
        )
        
        # Give it time to start and capture any startup errors
        time.sleep(2)
        
        # Check if process is still running
        if backend_process.poll() is not None:
            output, _ = backend_process.communicate()
            print("Backend process exited with error:")
            print(output)
            raise RuntimeError("Backend failed to start")
        
        return backend_process
    except Exception as e:
        print(f"Failed to start backend: {e}")
        raise

if __name__ == "__main__":
    # If this is a backend subprocess, run the backend directly
    if is_subprocess():
        # Import and run the backend directly
        from backend.main import app
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
        sys.exit(0)
    
    # Register signal handler for clean shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        backend_process = start_backend()
        print(f"Backend process started: {backend_process}")
        print("Opening PyWebView window...")
        
        # Create and show the webview
        webview.create_window(
            title="My Application",
            url="http://127.0.0.1:8000",
            width=1200,
            height=800
        )
        webview.start(debug=True)
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        # Cleanup: terminate backend when closing the app
        if backend_process:
            try:
                backend_process.terminate()
                backend_process.wait(timeout=3)
            except:
                try:
                    backend_process.kill()
                except:
                    pass
