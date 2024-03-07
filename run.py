#!/usr/bin/env python3
"""The run script"""

# import flywheel
from flywheel import GearContext
import logging
import os
import shutil
# import json
# import subprocess
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

    output_path = context.output_dir  # OUTPUT_DIR

    # Check input filenames (nnUNet format (_0000.nii.gz))
    rename_and_copy_file(input_file, output_path)


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
