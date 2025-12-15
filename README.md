# SC DL RESCUE - CLI Audio Downloader

SC DL RESCUE is a command-line interface tool designed to easily download audio from SoundCloud. It features a user-friendly interactive menu to handle tracks, playlists, and user uploads with flexible download options.

## Features

*   **Interactive CLI**: Built with `questionary` for a seamless user experience.
*   **URL Validation**: Automatically validates SoundCloud URLs (Tracks, Playlists, Users) before processing.
*   **Flexible Download Scopes**:
    *   **Download All Tracks**: Retrieve every track from a playlist or user.
    *   **Download a Range**: Specify a range (e.g., `1-5`) to download specific tracks.
    *   **Download Single Track**: Download just one track.
*   **Format Selection**: Choose between `mp3` or `best available` audio quality.
*   **Custom Output**: Define your own download directory (defaults to `downloads`).
*   **Fetch Limits**: Set a maximum number of tracks to fetch to save time.
*   **Cross-Platform**: Clears console appropriately on both Windows and Linux/macOS.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd soundcloud_downloader
    ```

2.  **Install dependencies:**
    This project requires Python 3. Install the necessary packages:
    ```bash
    pip install questionary
    ```
    *(Note: Ensure other dependencies required by `downloader` and `utils` are also installed).*

## Usage

Run the main application script:

```bash
python src/main.py
```

### Interactive Workflow

1.  **Enter URL**: Paste a valid SoundCloud URL when prompted.
2.  **Select Format**: Choose your desired audio format.
3.  **Set Directory**: Press Enter to use the default `downloads` folder or type a custom path.
4.  **Select Scope**: Choose to download all tracks, a specific range, or a single track.
5.  **Set Limit**: Optionally limit the number of tracks to process.

## Project Structure

- `src/main.py`: Main entry point handling user interaction and flow.
- `src/downloader.py`: Core logic for downloading content.
- `src/utils.py`: Utilities for fetching and parsing SoundCloud data.