import os
from PIL import Image
import pillow_heif
import zipfile
import shutil

def heic_to_jpg(heic_path, jpg_path):
    # Open HEIC file using pillow_heif
    image = pillow_heif.read_heif(heic_path)
    pil_image = Image.frombytes(image.mode, image.size, image.data)
    
    # Save as JPEG
    pil_image.save(jpg_path, "JPEG")

def unzip_photos(directory):
    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.startswith("Photos") and filename.lower().endswith(".zip"):
            zip_path = os.path.join(directory, filename)
            extract_dir = os.path.join(directory, os.path.splitext(filename)[0])
            
            # Unzip the file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Move HEIC files to the main directory
            for root, _, files in os.walk(extract_dir):
                for file in files:
                    if file.lower().endswith(".heic"):
                        shutil.move(os.path.join(root, file), os.path.join(directory, file))
            
            # Delete the zip file and the extracted directory
            os.remove(zip_path)
            shutil.rmtree(extract_dir)

def convert_and_zip(directory):
    jpg_files = []
    
    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.lower().endswith(".heic"):
            heic_path = os.path.join(directory, filename)
            jpg_filename = os.path.splitext(filename)[0] + ".jpg"
            jpg_path = os.path.join(directory, jpg_filename)
            
            # Convert HEIC to JPG
            heic_to_jpg(heic_path, jpg_path)
            jpg_files.append(jpg_path)
    
    zip_path = os.path.join(directory, "images.zip")
    
    # Create a zip file and add all JPG files
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for jpg_file in jpg_files:
            zipf.write(jpg_file, os.path.basename(jpg_file))
            os.remove(jpg_file)  # Optionally remove the jpg files after zipping

    print(f"Created {zip_path}")

def process_photos(directory):
    # Step 1: Unzip and process photos
    unzip_photos(directory)
    
    # Step 2: Convert HEIC to JPEG and zip
    convert_and_zip(directory)

# Example usage
process_photos('/Users/chadunderhill/Downloads')