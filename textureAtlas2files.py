"""
Texture Atlas Extraction and Sprite Sheet Generation Script

This script is designed to perform the following tasks:
1. Extract individual subtextures from a given texture atlas using an XML file
2. Save the extracted subtextures as individual PNG files in a specified directory
3. Optionally, generate a converted sprite sheet from the extracted subtextures

The script accepts command-line arguments for the XML file, the original texture atlas image, and the output directory. When creating a sprite sheet, it distributes the images in a rectangular shape.

Usage:
1. Extract subtextures:
   python script.py xml_file atlas_image output_dir

2. Optionally, generate a converted sprite sheet:
   python script.py xml_file atlas_image output_dir (answer "y" to the prompt)

Ensure that the required libraries (Pillow) are installed.
"""

import os
import argparse
import xml.etree.ElementTree as ET
from PIL import Image

def extract_subtextures(xml_file, atlas_image_path, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the texture atlas image outside the loop
    atlas_image = Image.open(atlas_image_path)

    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Iterate through the SubTexture elements in the XML
    for subtexture in root.findall(".//SubTexture"):
        name = subtexture.get("name")
        x = int(subtexture.get("x"))
        y = int(subtexture.get("y"))
        width = int(subtexture.get("width"))
        height = int(subtexture.get("height"))

        # Crop the subtexture from the atlas
        subtexture_image = atlas_image.crop((x, y, x + width, y + height))

        # Ensure the subtexture file has the .png extension
        if not name.endswith(".png"):
            name += ".png"

        # Save the subtexture as an individual image
        subtexture_image.save(os.path.join(output_dir, name))

    print("Subtextures extracted and saved to", output_dir)

def get_max_width_height_from_xml(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Initialize variables to store the largest width and height
    largest_width = 0
    largest_height = 0

    # Iterate through the SubTexture elements in the XML
    for subtexture in root.findall(".//SubTexture"):
        width = int(subtexture.get("width"))
        height = int(subtexture.get("height"))

        # Update the largest width and height if necessary
        largest_width = max(largest_width, width)
        largest_height = max(largest_height, height)

    return largest_width, largest_height

def generate_sprite_sheet(xml_file, output_dir, original_filename):
    largest_width, largest_height = get_max_width_height_from_xml(xml_file)

    # Get a list of individual subtexture files in the output directory
    subtexture_files = [file for file in os.listdir(output_dir) if file.endswith(".png")]

    # Calculate the number of rows and columns based on the largest dimension
    if largest_width >= largest_height:
        num_columns = int((sum(1 for _ in subtexture_files)) ** 0.5)
        num_rows = (sum(1 for _ in subtexture_files) // num_columns) + 1
    else:
        num_rows = int((sum(1 for _ in subtexture_files)) ** 0.5)
        num_columns = (sum(1 for _ in subtexture_files) // num_rows) + 1

    # Calculate sprite sheet dimensions
    sprite_sheet_width = largest_width * num_columns
    sprite_sheet_height = largest_height * num_rows

    # Create an empty sprite sheet image
    sprite_sheet = Image.new("RGBA", (sprite_sheet_width, sprite_sheet_height))

    for i, subtexture_file in enumerate(subtexture_files):
        subtexture_image = Image.open(os.path.join(output_dir, subtexture_file))

        # Calculate position for pasting the subtexture
        x = (i % num_columns) * largest_width
        y = (i // num_columns) * largest_height

        # Paste the subtexture onto the sprite sheet
        sprite_sheet.paste(subtexture_image, (x, y))

    # Save the sprite sheet with the "_converted" suffix
    converted_filename = os.path.splitext(original_filename)[0] + "_converted.png"
    converted_filepath = os.path.join(output_dir, converted_filename)
    sprite_sheet.save(converted_filepath)
    print(f"Sprite sheet saved as {converted_filename} in {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract subtextures and optionally generate a converted sprite sheet.")
    parser.add_argument("xml_file", help="Path to the texture atlas XML file")
    parser.add_argument("atlas_image", help="Path to the original texture atlas image (PNG)")
    parser.add_argument("output_dir", help="Path to the output directory for subtextures and sprite sheets")
    parser.add_argument("--export-spritesheet", action="store_true", help="Export the generated sprite sheet without user input")

    args = parser.parse_args()

    # Extract subtextures
    extract_subtextures(args.xml_file, args.atlas_image, args.output_dir)

    # Automatically generate and export a sprite sheet if the flag is set
    if args.export_spritesheet:
        generate_sprite_sheet(args.xml_file, args.output_dir, os.path.basename(args.atlas_image))
    else:
        # Ask the user if they want to create a sprite sheet
        create_sprite_sheet = input("Do you want to create a converted sprite sheet? (y/n): ")
        if create_sprite_sheet.lower() == 'y':
            generate_sprite_sheet(args.xml_file, args.output_dir, os.path.basename(args.atlas_image))
