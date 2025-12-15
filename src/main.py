from downloader import Downloader
import questionary
import os
import platform 
from utils import fetch_tracks 

def clear_console():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def display_logo():
    # ANSI Colors
    # \033[38;5;202m is the specific SoundCloud Orange
    # \033[1m is Bold
    # \033[0m is Reset
    O = "\033[38;5;202m" 
    B = "\033[1m"
    R = "\033[0m"

    logo = f"""
{O}       ▄▄▄▄▄▄▄{R}
{O}     █ █       █  {B}SC DL RESCUE{R}
{O}   █ █ █       █  {R}CLI Audio Downloader
{O}   █ █ █       █  {R}
{O}   ▀ ▀ ▀▀▀▀▀▀▀▀▀  {R}
    """
    print(logo)
    print("Welcome to SC DL Rescue CLI Audio Downloader!\n")
def main():
    clear_console() 

    while True:
        display_logo() 

        url = None
        while not url:
            entered_url = questionary.text("Enter the SoundCloud URL (track, playlist, or user, or 'q' to quit):").ask()
            if entered_url and entered_url.lower() == 'q':
                print("Exiting application.")
                return

            if not entered_url:
                print("URL cannot be empty. Please try again.")
                continue

            print("Validating URL...")
            fetched_info = fetch_tracks(entered_url, limit=1) 
            if fetched_info:
                url = entered_url
                print("URL validated successfully.")
            else:
                print("Invalid or un-fetchable URL. Please check the URL and try again.")

        download_format = questionary.select(
            "Select download format:",
            choices=["mp3", "best available"],
            default="mp3"
        ).ask()

        download_dir = questionary.text(
            "Enter download directory:",
            default="downloads"
        ).ask()
        
        if not download_dir:
            download_dir = "downloads"
        os.makedirs(download_dir, exist_ok=True)

        download_type_choice = questionary.select(
            "Select download scope:",
            choices=["Download All Tracks", "Download a Range of Tracks", "Download a Single Track"],
            default="Download All Tracks"
        ).ask()

        track_range = None
        if download_type_choice == "Download a Range of Tracks":
            track_range = questionary.text(
                "Enter track range (e.g., '1-20'):"
            ).ask()
            if not track_range:
                print("Track range cannot be empty. Proceeding with all tracks.")
                track_range = None 
        elif download_type_choice == "Download a Single Track":
            track_range = "1-1" 

        limit_input = questionary.text(
            "Enter maximum number of tracks to fetch (leave empty for unlimited):",
            default="" 
        ).ask()
        limit = None 
        if limit_input: 
            try:
                limit = int(limit_input)
            except ValueError:
                print("Invalid limit, defaulting to unlimited.")
                limit = None 
        
        downloader = Downloader(url, download_format, download_dir, track_range, limit)
        try:
            downloader.download()
        except KeyboardInterrupt:
            pass 
        except Exception as e:
            print(f"\nAn error occurred during the download: {e}")

        print("\nDownload process finished or cancelled.")
        if not questionary.confirm("Do you want to start another download?").ask():
            print("Exiting application.")
            break
        
        clear_console() 

if __name__ == "__main__":
    main()