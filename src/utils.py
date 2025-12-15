import json
import subprocess

def fetch_tracks(url, limit):
    try:
        command = [
            "yt-dlp",
            "--no-progress",
            "--flat-playlist",
            "--print",
            "%(webpage_url)s <|SEP|> %(title)s <|SEP|> %(uploader)s",
        ]
        if limit is not None:
            command.extend(["--playlist-items", f"1-{limit}"])
        command.append(url)
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        tracks = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split(' <|SEP|> ')
                if len(parts) == 3:
                    url_val, title, artist = parts
                    
                    # Fallback: Extract metadata from URL if yt-dlp returns NA
                    if (title == "NA" or artist == "NA") and url_val != "NA":
                        try:
                            # Clean URL and extract parts: soundcloud.com/artist/title-slug
                            clean_url = url_val.split('?')[0].strip('/')
                            url_parts = clean_url.split('/')
                            if len(url_parts) >= 2:
                                if title == "NA": title = url_parts[-1].replace('-', ' ').title()
                                if artist == "NA": artist = url_parts[-2].replace('-', ' ').title()
                        except Exception: pass

                    tracks.append({"url": url_val, "title": title, "artist": artist if artist != "NA" else "Unknown Artist"})
        return tracks
    except FileNotFoundError:
        print("yt-dlp not found, trying with scdl...")
        return fetch_tracks_scdl(url, limit)
    except subprocess.CalledProcessError as e:
        print(f"yt-dlp failed with error: {e.stderr}")
        print("Trying with scdl...")
        return fetch_tracks_scdl(url, limit)
    except Exception as e:
        print(f"An unexpected error occurred with yt-dlp: {e}")
        print("Trying with scdl...")
        return fetch_tracks_scdl(url, limit)

def fetch_tracks_scdl(url, limit):
    try:
        command = [
            "scdl",
            "-l",
            url,
            "--dump-json",
        ]
        if limit is not None:
            command.extend(["-n", str(limit)])
        
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            encoding='utf-8'
        )
        try:
            stdout, stderr = process.communicate(timeout=300)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            raise Exception(f"scdl timed out. stderr: {stderr}")

        if process.returncode != 0:
            raise Exception(stderr)

        tracks_to_download = []
        for line in stdout.strip().split('\n'):
            if line:
                track_info = json.loads(line)
                tracks_to_download.append({
                    "url": track_info["permalink_url"], 
                    "title": track_info["title"],
                    "artist": track_info.get("user", {}).get("username", "Unknown Artist") # Extract artist
                })
        return tracks_to_download
    
    except Exception as e:
        print(f"scdl also failed: {e}. Could not fetch playlist details.")
        return []
