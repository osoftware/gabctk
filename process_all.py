#!/usr/bin/env python3
import os
import sys
import glob
import subprocess
from pathlib import Path

def process_gabc_files(input_dir, output_dir, tempo=100):
    # Convert to absolute paths
    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)
    
    # Find all .gabc files recursively
    for gabc_path in glob.glob(os.path.join(input_dir, '**/*.gabc'), recursive=True):
        # Get the relative path to maintain directory structure
        rel_path = os.path.relpath(gabc_path, input_dir)
        # Create the output path with same structure
        output_path = os.path.join(output_dir, os.path.splitext(rel_path)[0] + '.mid')
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        print(f"Processing {gabc_path}")
        
        # Run gabctk.py with appropriate parameters
        try:
            subprocess.run([
                sys.executable,
                'gabctk.py',
                '-i', gabc_path,
                '-o', output_path,
                '-t', str(tempo)
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error processing {rel_path}: {e}", file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: process_all.py <input_directory> <output_directory>")
        print("Example: process_all.py ../graduale/gabc ../kendronale/assets")
        sys.exit(1)
        
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    if not os.path.isdir(input_dir):
        print(f"Error: Input directory {input_dir} does not exist", file=sys.stderr)
        sys.exit(1)
        
    process_gabc_files(input_dir, output_dir)