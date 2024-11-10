import os
import webbrowser
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

class VisualizationHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.html'):
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] New visualization: {os.path.basename(event.src_path)}")
            try:
                webbrowser.open(f"file://{os.path.abspath(event.src_path)}")
                print(f"✓ Opened in browser: {event.src_path}")
            except Exception as e:
                print(f"! Error opening browser: {str(e)}")

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.html'):
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Updated: {os.path.basename(event.src_path)}")

def monitor_visualizations():
    visualizations_dir = "visualizations"
    
    if not os.path.exists(visualizations_dir):
        os.makedirs(visualizations_dir)
        print(f"\nCreated directory: {visualizations_dir}")
    
    print("\n=== Visualization Monitor ===")
    print(f"Directory: {os.path.abspath(visualizations_dir)}")
    print("Status: Active - Waiting for new visualizations...")
    print("\nCurrent files:")
    for file in os.listdir(visualizations_dir):
        if file.endswith('.html'):
            print(f"- {file}")
    
    print("\nMonitoring for changes...")
    
    event_handler = VisualizationHandler()
    observer = Observer()
    observer.schedule(event_handler, visualizations_dir, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping visualization monitor...")
    observer.join()

if __name__ == "__main__":
    monitor_visualizations()git 