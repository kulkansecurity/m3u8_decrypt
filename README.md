# m3u8_decrypt.py – PoC for decrypting HLS Streams 

## Features 

`m3u8_decrypt.py` is a PoC script in python that can be used to **automate the download and decryption** of encrypted HLS (HTTP Live Streaming) media content. It reads `.m3u8` playlists, fetches encrypted `video segments` and their corresponding `encryption key` files, and outputs decrypted `.ts` files ready for playback or further processing. 

The script was released along with a Blog post on Watermark bypasses, available at:
- https://blog.kulkan.com/bypassing-watermark-implementations-fe39e98ca22b

## Installation 

This tool depends on the following Python libraries: 
- `requests` 
- `cryptography` 

Install them with: ``` pip install requests cryptography ``` 

Just clone/download the script and run it.

## Usage 

``` python3 m3u8_decrypt.py ``` 

The script will prompt you for: 

1. **.m3u8 file URL** (e.g., `https://example.com/playlist/index.m3u8`) 
2. **Base URL for .key files** (e.g., `https://example.com/playlist/`) 

Once provided, it will: 
- Download the `.m3u8` playlist. 
- Identify all `.ts.enc` segments. 
- Download each encrypted segment and its corresponding `.key` file. 
- Decrypt each segment into a `.ts` file. 
- Save encrypted and decrypted files to: 
- `./encrypted_files/` 
- `./decrypted_files/` 

If authentication is required (e.g., JWT or cookies), you can configure them in the script by editing the `jwt` and `cookies` variables in the `main()` function.

# Legal Notice
It is your responsibility to ensure you're allowed to access and decrypt the content. Use of this tool must comply with applicable copyright laws, DRM regulations, and service terms. Unauthorized decryption or redistribution of protected content is prohibited. 
