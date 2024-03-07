#!/usr/bin/env python3
"""The run script"""

# import flywheel
from flywheel import GearContext
import logging
import os
# import glob
# import shutil
# import subprocess
# import zipfile
# import json

from fw_gear_aeye.parser import parse_config

# log = logging.getLogger(__name__)

# DEFINE VARIABLES
FLYWHEEL_BASE = "/flywheel/v0"
MANIFEST_FILE = os.path.join(FLYWHEEL_BASE, "manifest.json")
CONFIG_FILE = os.path.join(FLYWHEEL_BASE, "config.json")
INPUT_DIR = os.path.join(FLYWHEEL_BASE, "input", "nifti")
ROOTOUT_DIR = os.path.join(FLYWHEEL_BASE, "output")
OUTPUT_DIR = os.path.join(ROOTOUT_DIR, "out")
WORKING_DIR = os.path.join(ROOTOUT_DIR, "work")
# CONTAINER = '[flywheel/aeye]'

# ----------------------------------------------------------------------------------------------
# MAIN FUNCTION


def main(context: GearContext) -> None:
    ''' Parse config and run'''

    # Call parse_config to extract the args, kwargs from the context
    # (e.g. config.json).
    input_file, config_measurement, config_debug = parse_config(
        context
    )

    # log.debug(f"input-file: {input_file}")

    # output_path = context.output_dir  # OUTPUT_DIR

    # # nnUNet
    # shm_size = 10 # shared memory (gb)
    # abs_path = '/mnt/sda1/Repos/a-eye/a-eye_segmentation/deep_learning/nnUNet/nnUNet'
    # rel_path = '/opt/nnunet_resources'
    # aux_in = f'nnUNet_inference/temp_inference/input' # input aux folder
    # aux_out = f'nnUNet_inference/temp_inference/output' # output aux folder

    # Check input filenames (nnUNet format (_0000.nii.gz))
    check_filename(input_file)


def check_filename(file):
    file_extensions = []
    while True:
        file_path, ext = os.path.splitext(file)
        if ext:
            file_extensions.insert(0, ext)
        else:
            break
    file_extension = ''.join(file_extensions)
    file_name = os.path.basename(file_path)
    file_path = f'{file_path}{file_extension}'
    # log.debug(f'[AEye] file name: {file_name}')
    # log.debug(f'[AEye] file extension: {file_extension}')
    # log.debug(f'[AEye] absolute file path: {file_path}')
    if not str(file_name).endswith('_0000'):
        correct_filename(file_path, file_name, file_extension)


def correct_filename(file_path, file_name, file_extension):
    # log.debug('[AEye] Changing filename to nnUNet format...')
    new_file_name = f'{file_name}_0000{file_extension}'  # extension for nnUNet
    os.rename(
        file_path,
        os.path.join(OUTPUT_DIR, new_file_name)
    )


# Only execute if file is run as main, not when imported by another module
if __name__ == "__main__":
    # Get access to gear config, inputs, and sdk client if enabled.
    with GearContext() as gear_context:
        # Initialize logging, set logging level based on `debug` configuration
        # key in gear config.
        gear_context.init_logging()

        # Pass the gear context into main function defined above.
        main(gear_context)
