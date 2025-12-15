import json
import subprocess

def fetch_tracks(url, limit):
    try:
        command = [
            "yt-dlp",
            "--dump-json",
            "--no-progress",
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
                track_info = json.loads(line)
                tracks.append({"url": track_info.get("webpage_url"), "title": track_info.get("title"), "artist": track_info.get("artist") or track_info.get("uploader") or "Unknown Artist"})
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
