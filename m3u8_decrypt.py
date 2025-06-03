# Sebastian Savini <ssavini@kulkan.com>
# June 3rd, 2025.
import os
import requests
from pathlib import Path
from urllib.parse import urljoin
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


# Function to download a file from a URL
def download_file(url, destination_file, headers=None, cookies=None):
    try:
        print(f"Downloading: {url}")
        response = requests.get(url, headers=headers, cookies=cookies, timeout=30)
        response.raise_for_status()
        with open(destination_file, 'wb') as f:
            f.write(response.content)
        print(f"File downloaded successfully: {destination_file}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        raise


# Function to read the key file
def read_key(key_file):
    with open(key_file, 'rb') as f:
        return f.read()


# Function to decrypt an encrypted .ts.enc segment
def decrypt_segment(enc_file, decrypted_file, key, iv=None):
    if len(key) != 16:
        raise ValueError("The key must be 16 bytes (128 bits).")
    
    with open(enc_file, 'rb') as f_enc, open(decrypted_file, 'wb') as f_out:
        encrypted_data = f_enc.read()
        iv = iv or encrypted_data[:16]  # Use the first 16 bytes as IV if not provided
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data[16:]) + decryptor.finalize()
        f_out.write(decrypted_data)


# Function to process the .m3u8 file from the given URL
def process_m3u8(m3u8_url, base_key_url, decrypted_dir, encrypted_dir, headers=None, cookies=None):
    # Local name to save the downloaded .m3u8 file
    local_m3u8_file = './downloaded_playlist.m3u8'

    # Download the .m3u8 file
    download_file(m3u8_url, local_m3u8_file, headers=headers, cookies=cookies)

    # Read and process the .m3u8 file
    with open(local_m3u8_file, 'r') as f:
        lines = f.readlines()

    # Create output directories for encrypted and decrypted files if they don't exist
    Path(decrypted_dir).mkdir(parents=True, exist_ok=True)
    Path(encrypted_dir).mkdir(parents=True, exist_ok=True)

    segments = []

    # Process the lines in the .m3u8 file
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.endswith('.ts.enc'):
            segments.append(line)

    # Base URL to resolve segment URLs
    base_url = m3u8_url.rsplit('/', 1)[0] + '/'

    # Download and decrypt each segment
    for segment in segments:
        segment_url = urljoin(base_url, segment)
        enc_file = os.path.join(encrypted_dir, segment)

        # Download the encrypted segment if it doesn't exist
        if not os.path.exists(enc_file):
            download_file(segment_url, enc_file, headers=headers, cookies=cookies)

        # Generate the name for the decrypted file
        decrypted_name = segment.replace('.ts.enc', '.ts')
        decrypted_file = os.path.join(decrypted_dir, decrypted_name)

        # Download the associated key
        key_url = urljoin(base_key_url, segment.replace('.ts.enc', '.key'))
        key_file = os.path.join(encrypted_dir, os.path.basename(key_url))

        if not os.path.exists(key_file):
            download_file(key_url, key_file, headers=headers, cookies=cookies)

        # Read the key and decrypt the segment
        key = read_key(key_file)
        print(f"Decrypting: {enc_file}")
        decrypt_segment(enc_file, decrypted_file, key)
        print(f"Decrypted segment saved at: {decrypted_file}")

    print("Processing completed.")


# Main function

# Example m3u8 url file : https://cdn.theoplayer.com/video/big_buck_bunny_encrypted/stream-800/index.m3u8
# Example base key url: https://cdn.theoplayer.com/video/big_buck_bunny_encrypted/stream-800/

def main():
    # Prompt the user for the full URL of the .m3u8 file
    m3u8_url = input("Please enter the full URL of the .m3u8 file: ").strip()

    # Prompt the user for the base URL for keys
    base_key_url = input("Please enter the base URL for the keys: ").strip()

    # Output directories
    decrypted_dir = './decrypted_files/'  # For decrypted files
    encrypted_dir = './encrypted_files/'  # For encrypted files and keys

    # If we receive an unauthorized message, we probably need to configure the authentication method
    # Authentication: Headers and Cookies
    jwt = {
        'Authorization': 'Bearer YOUR_JWT_TOKEN_HERE',
    }
    cookies = {
        'sessionid': 'YOUR_SESSION_COOKIE_HERE',
    }

    try:
        # Process the .m3u8 file and handle keys and segments
        process_m3u8(m3u8_url, base_key_url, decrypted_dir, encrypted_dir, headers=jwt, cookies=cookies)
    except Exception as e:
        print(f"Error during processing: {e}")


if __name__ == "__main__":
    main()
