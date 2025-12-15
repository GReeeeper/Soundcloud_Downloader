import os
import subprocess
from utils import fetch_tracks
from tqdm import tqdm
import questionary # Still needed for initial confirmation

class Downloader:
    def __init__(self, url, download_format="mp3", download_dir="downloads", track_range=None, limit=200):
        self.url = url
        self.download_format = download_format
        self.download_dir = download_dir
        self.track_range = track_range
        self.limit = limit
        self.all_tracks = [] # Store all fetched tracks

    def download(self):
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        print("Fetching tracks for the provided URL...")
        self.all_tracks = fetch_tracks(self.url, self.limit)

        if not self.all_tracks:
            print("No tracks found or an error occurred while fetching tracks.")
            return

        tracks_to_download = []

        if self.track_range:
            try:
                start, end = map(int, self.track_range.split('-'))
                # Adjust for 0-based indexing and ensure bounds
                start_idx = max(0, start - 1)
                end_idx = min(len(self.all_tracks), end)
                tracks_to_download = self.all_tracks[start_idx:end_idx]
            except ValueError:
                print("Invalid range format. Please use 'start-end' (e.g., '1-20').")
                return
            except Exception as e:
                print(f"Error processing track range: {e}")
                return
        else:
            tracks_to_download = self.all_tracks
        
        if not tracks_to_download:
            print("No tracks selected for download.")
            return

        print("\n--- Tracks to be Downloaded ---")
        for i, track in enumerate(tracks_to_download):
            print(f"{i+1}. {track.get('title', 'Unknown Title')} by {track.get('artist', 'Unknown Artist')}")
        print("-------------------------------\n")

        confirmation = questionary.confirm(f"Proceed with downloading {len(tracks_to_download)} tracks?").ask()
        if not confirmation:
            print("Download cancelled by user.")
            return

        print(f"Starting download of {len(tracks_to_download)} tracks to '{self.download_dir}'...")
        
        try:
            for track in tqdm(tracks_to_download, desc="Overall Progress"):
                track_title = track.get('title', 'Unknown Title')
                track_artist = track.get('artist', 'Unknown Artist')
                tqdm.write(f"Downloading: {track_title} by {track_artist}")
                self._download_single(track['url'])
            
            tqdm.write("Download finished!")
        except KeyboardInterrupt:
            tqdm.write("\nDownload interrupted by user (Ctrl+C).")
            raise # Re-raise to be caught by main.py
        finally:
            # Ensure tqdm progress bar is properly closed
            # This is important if an interrupt happens mid-loop
            pass 
    
    def _download_single(self, track_url):
        command = [
            "scdl",
            "-l",
            track_url,
            "--path",
            self.download_dir,
        ]
        if self.download_format == "mp3":
            command.append("--onlymp3")
        # If format is "best available", no specific format flag is appended,
        # allowing scdl to download the default/best quality available.

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            encoding='utf-8'
        )
        try:
            stdout, stderr = process.communicate()
        except KeyboardInterrupt:
            process.terminate() # Terminate the scdl process
            tqdm.write(f"Terminating scdl process for {track_url}...")
            raise # Re-raise the KeyboardInterrupt

        if process.returncode != 0:
            tqdm.write(f"Error downloading {track_url}:")
            if stdout:
                tqdm.write(f"  stdout: {stdout.strip()}")
            if stderr:
                tqdm.write(f"  stderr: {stderr.strip()}")