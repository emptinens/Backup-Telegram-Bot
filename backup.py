import os
import zipfile
import requests
import curses
import time
from art import text2art

# Telegram bot details (Replace with your values)
BOT_TOKEN = "your_telegram_bot_token"
CHAT_ID = "your_chat_id"

def bloody_text():
    """Generate ASCII text with a bloody font."""
    return text2art("emptinens", font="bloody")

def animate_banner(stdscr):
    """Display the bloody ASCII banner and wait for user input."""
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()

    text_lines = bloody_text().split("\n")
    max_y, max_x = stdscr.getmaxyx()

    # Ensure text fits within screen bounds
    max_text_width = max(len(line) for line in text_lines)
    start_y = max(0, (max_y // 2) - (len(text_lines) // 2))  
    start_x = max(0, (max_x // 2) - (max_text_width // 2))  

    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    # Print the ASCII banner
    for i, line in enumerate(text_lines):
        if start_y + i < max_y:  
            stdscr.addstr(start_y + i, start_x, line[:max_x-1], curses.color_pair(1) | curses.A_BOLD)

    stdscr.refresh()

    # Wait for user input to continue
    stdscr.getch()


def zip_folder(folder_path, output_filename):
    """Compress the selected folder into a .zip file."""
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, arcname)
    print(f"✅ Folder zipped successfully: {output_filename}")

def send_to_telegram(file_path):
    """Send the zipped file to Telegram."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(file_path, "rb") as f:
        response = requests.post(url, data={"chat_id": CHAT_ID}, files={"document": f})
    if response.status_code == 200:
        print("✅ File sent successfully to Telegram!")
    else:
        print("❌ Failed to send file:", response.text)

if __name__ == "__main__":
    curses.wrapper(animate_banner)  # Show animated banner first

    folder = input("\nEnter the full path of the folder to zip: ").strip()
    
    # Expand `~` to the full home directory path
    folder = os.path.expanduser(folder)
    folder = os.path.abspath(folder)  # Normalize path

    print(f"🔍 Checking folder: {folder}")  # Debugging output
    
    if not os.path.exists(folder):
        print("❌ Error: Folder does not exist! Please check the path.")
    elif not os.path.isdir(folder):
        print("❌ Error: The provided path is not a directory!")
    else:
        zip_name = os.path.join(os.path.dirname(folder), f"{os.path.basename(folder)}.zip")
        zip_folder(folder, zip_name)
        send_to_telegram(zip_name)

