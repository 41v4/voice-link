import sys
import threading
from queue import Queue

from PySide6.QtWidgets import QApplication

from client.main import MainWindow
from server.api import app

# Shared queue
shared_queue = Queue()

def run_server():
    app.config['shared_queue'] = shared_queue
    app.run(debug=False, port=5000, use_reloader=False)

if __name__ == "__main__":
    # Server thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    # GUI Application
    app = QApplication(sys.argv)
    window = MainWindow(shared_queue)
    window.show()
    sys.exit(app.exec())
