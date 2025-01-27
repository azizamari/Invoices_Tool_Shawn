import threading
import webview
import subprocess


def start_streamlit():
    """Function to run the Streamlit app."""
    app_path = "D:/work/upwork/armstrong/src/app.py"
    streamlit_path = r"D:\work\upwork\armstrong\env\Scripts\streamlit.exe"  

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    subprocess.Popen(
        [streamlit_path, "run", app_path, "--server.headless", "true"],
        startupinfo=startupinfo, 
        creationflags=subprocess.CREATE_NO_WINDOW
    )


def start_webview():
    """Function to create a webview window."""
    webview.create_window("Invoice Extraction App", "http://localhost:8501")
    webview.start()


if __name__ == "__main__":
    threading.Thread(target=start_streamlit, daemon=True).start()
    start_webview()
