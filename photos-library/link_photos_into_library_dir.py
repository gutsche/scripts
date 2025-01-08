# -*- coding: utf-8 -*-

"""
script to symbolically link every photo found in input directory in output directory reproducing sub-directory structure
"""

# Import required modules
import os
import sys
import argparse
import logging

def link_photos():
    """
    script to symbolically link every photo found in input directory in output directory reproducing sub-directory structure
    """

    parser = argparse.ArgumentParser(description='script to symbolically link every photo found in input directory in output directory reproducing sub-directory structure')

    # Add required arguments for input and output directories as strings
    parser.add_argument('--input_dir', required=True, type=str, help='Path to the input directory containing photos')
    parser.add_argument('--output_dir', required=True, type=str, help='Path to the output directory where symbolic links will be created')
    parser.add_argument('--log_file', default=None, type=str, help='file with log output')
    parser.add_argument('--file_extensions', default='xmp,jpg', type=str, help='comma separated list of file extensions to be processed (e.g., txt,pdf,jpg)')
    parser.add_argument('--extension_analysis', action='store_true', help='Perform extension analysis on the input data and return', default=False)
    # Add optional verbosity control flag
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase verbosity (e.g., -vv for even more verbose)')

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    # file extensions
    file_extensions = args.file_extensions.split(',')
    extension_analysis = args.extension_analysis

    # remove stream handler from root logger
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            root_logger.removeHandler(handler)
    # Create a console logger
    logger = logging.getLogger(__name__)
    console_logger = logging.StreamHandler()
    formatter = logging.Formatter(
            "[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",)
    console_logger.setFormatter(formatter)
    logger.addHandler(console_logger)

    # Create a file logger (e.g., for persistent logging to a file)
    if args.log_file != None:
        logger.info("Logging enabled with file: {}".format(args.log_file))
        file_logger = logging.FileHandler(args.log_file, mode='w')  # Specify the log file path
        file_logger.setFormatter(formatter)
        logger.addHandler(file_logger)    

    logger.warning("Making symbolic links of all files in input_dir {} with file extensions {} in same directory tree in output_dir {}.".format(args.input_dir, ','.join(file_extensions), args.output_dir))

    if extension_analysis:

        # Initialize an empty set to store unique file extensions
        local_file_extensions = set()

        # Traverse the directory and its subdirectories
        for root, dirs, files in os.walk(args.input_dir):
            for file in files:
                if not file.startswith('.') and not os.path.basename(root).startswith('.'):
                    # Get the file extension (e.g., '.txt', '.pdf', etc.)
                    _, extension = os.path.splitext(file)
                    # Add the file extension to the set
                    file_extension = extension.lstrip('.')
                    local_file_extensions.add(file_extension)
        
        logger.warning("Extension currently considered: {}".format(sorted(file_extensions)))
        logger.warning("File extensions found in input directory: {}".format(sorted(list(local_file_extensions))))
        sys.exit(0)

    # Iterate over all files and subdirectories in input_dir
    for root, dirs, files in os.walk(args.input_dir):
        rel_path = os.path.relpath(root, args.input_dir)
        
        # Create the corresponding path in output_dir
        output_path = os.path.join(args.output_dir, *rel_path.split(os.sep))
        
        # Make sure we create all directories that are above our target directory
        for subdir in dirs:
            subdir_path = os.path.join(output_path, subdir)
            os.makedirs(subdir_path, exist_ok=True)

    # Iterate over all files in input_dir
    for root, dirs, files in os.walk(args.input_dir):
        rel_path = os.path.relpath(root, args.input_dir)
        
        # Create the corresponding path in output_dir
        output_path = os.path.join(args.output_dir, *rel_path.split(os.sep))
        
        for file in files:

            # Get the file extension (e.g., '.txt', '.pdf', etc.)
            _, extension = os.path.splitext(file)
            # Add the file extension to the set
            file_extension = extension.lstrip('.')

            # continue if file extension is in the set of allowed file extensions
            if file_extension in file_extensions:

                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(output_path, file)
                
                # If the file is already present, remove it
                if os.path.exists(output_file_path):
                    os.remove(output_file_path)

                # Make symbolic link to the original file
                os.symlink(input_file_path, output_file_path)

    # Return exit code to the operating system
    sys.exit(0)

if __name__ == "__main__":
    link_photos()