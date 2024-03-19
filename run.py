#!/usr/bin/env python3
"""The run script"""

# import flywheel
from flywheel import GearContext
import logging
import os
import shutil
from pathlib import Path
import subprocess
import sys
import time
# import json
# import zipfile

from fw_gear_aeye.parser import parse_config

log = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------------
# MAIN FUNCTION


def main(context: GearContext) -> None:
    ''' Parse config and run'''

    # Call parse_config to extract the args, kwargs from the context
    # (e.g. config.json).
    input_file, config_measurement, config_debug = parse_config(
        context
    )

    log.debug(f"input-file: {input_file}")
    log.debug(f"measurement: {config_measurement}")
    log.debug(f"debug: {config_debug}")

    output_dir = context.output_dir  # OUTPUT_DIR
    work_dir = context.work_dir  # WORK_DIR

    # Check input filenames (nnUNet format (_0000.nii.gz))
    rename_and_copy_file(input_file, work_dir)


    # Command
    cmd = [
        "nnUNet_predict",
        "-i",
        str(work_dir),
        "-o",
        str(output_dir),
        "-tr",
        "nnUNetTrainerV2",
        "-ctr",
        "nnUNetTrainerV2CascadeFullRes",
        "-m",
        "3d_fullres",
        "-p",
        "nnUNetPlansv2.1",
        "-t",
        "Task313_Eye"
    ]

    log.info(f"Calling...\n{' '.join(cmd)}")

    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE  # cwd="."
    )


    # Stream the output from p.communicate so the user can monitor the progress continuously.
    # This approach is taken from:
    # https://gitlab.com/flywheel-io/flywheel-apps/nifti-to-dicom/-/blob/0.1.0/fw_gear_nifti_to_dicom/pixelmed.py
    while True:
        time.sleep(5)
        if process.poll() is None:
            output, _ = process.communicate()
            print(output.decode("utf-8").strip() + "\n")
        else:
            if process.returncode != 0:
                log.error(
                    f"AEye segmentation failed with exit_code: {process.returncode}"
                )
                raise SystemExit(1)
            else:
                log.info("AEye segmentation completed")
                subprocess.call(cmd)
                sys.exit(process.returncode)


# ----------------------------------------------------------------------------------------------
# FUNCTIONS


def rename_and_copy_file(original_path, new_path):
    """
    Rename a file and copy it to another folder.

    Args:
        original_path (str): The path to the original file.
        new_path (str): The path to the destination folder.

    Returns:
        str: The path to the copied file in the destination folder.
    """

    # Get the old and new names
    old_name = os.path.basename(str(original_path)).split(".")[0]
    new_name = old_name + "_0000" + ".nii.gz"

    # Create new directory
    os.makedirs(new_path, exist_ok=True)

    # Construct the new path with the new name
    new_path = os.path.join(new_path, new_name)
    log.debug(f"changed filename: {new_path}")

    # Rename and copy the file
    shutil.copy2(original_path, new_path)


# Only execute if file is run as main, not when imported bu another module
if __name__ == "__main__":
    # Get access to gear config, inputs and sdk client if enabled
    with GearContext() as gear_context:
        # Initialize logging, set logging level based on `debug` configuration
        gear_context.init_logging()
        # Pass the gear context into main function defined above
        main(gear_context)
