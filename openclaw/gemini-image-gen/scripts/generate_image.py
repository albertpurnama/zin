#!/usr/bin/env python3
"""
Generate images using Google's Gemini API.
Usage: python generate_image.py "prompt" [--output filename] [--aspect-ratio RATIO] [--size SIZE]
"""

import argparse
import mimetypes
import os
import sys
from google import genai
from google.genai import types


def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)
    print(f"File saved to: {file_name}")
    return file_name


def generate_image(prompt, output_name="generated_image", aspect_ratio="1:1", size="1K", api_key=None):
    """
    Generate an image using Gemini API.
    
    Args:
        prompt: Text description of the image to generate
        output_name: Base name for the output file (without extension)
        aspect_ratio: Aspect ratio (e.g., "1:1", "16:9", "4:3", "3:4", "9:16")
        size: Image size (e.g., "1K", "2K", "4K")
        api_key: Gemini API key (defaults to GEMINI_API_KEY env var)
    
    Returns:
        Path to the generated image file
    """
    client = genai.Client(
        api_key=api_key or os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-3-pro-image-preview"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        image_config=types.ImageConfig(
            aspect_ratio=aspect_ratio,
            image_size=size,
        ),
        response_modalities=[
            "IMAGE",
            "TEXT",
        ],
    )

    file_index = 0
    saved_files = []
    
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.parts is None:
            continue
        if chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
            file_name = f"{output_name}_{file_index}" if file_index > 0 else output_name
            file_index += 1
            inline_data = chunk.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type) or ".png"
            full_path = f"{file_name}{file_extension}"
            save_binary_file(full_path, data_buffer)
            saved_files.append(full_path)
        else:
            text = chunk.text
            if text:
                print(text)
    
    return saved_files


def main():
    parser = argparse.ArgumentParser(description="Generate images using Gemini API")
    parser.add_argument("prompt", help="Text description of the image to generate")
    parser.add_argument("--output", "-o", default="generated_image", help="Output filename (without extension)")
    parser.add_argument("--aspect-ratio", "-a", default="1:1", 
                        choices=["1:1", "16:9", "4:3", "3:4", "9:16"],
                        help="Aspect ratio of the generated image")
    parser.add_argument("--size", "-s", default="1K",
                        choices=["1K", "2K", "4K"],
                        help="Image size/resolution")
    parser.add_argument("--api-key", help="Gemini API key (or set GEMINI_API_KEY env var)")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set. Provide --api-key or set environment variable.")
        sys.exit(1)
    
    files = generate_image(
        prompt=args.prompt,
        output_name=args.output,
        aspect_ratio=args.aspect_ratio,
        size=args.size,
        api_key=api_key
    )
    
    if files:
        print(f"\nGenerated {len(files)} image(s):")
        for f in files:
            print(f"  - {f}")
    else:
        print("No images were generated.")


if __name__ == "__main__":
    main()
