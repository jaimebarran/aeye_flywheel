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

# nnUNet
input_folder_nnunet = '/input'  # folder with the images to segment
output_folder_nnunet = '/output'  # folder with the segmentations


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
    dest_path = output_path + input_folder_nnunet
    rename_and_copy_file(input_file, dest_path)

    # Get nnUNet dir
    nnunet_dir = get_nnunet_dir()
    print("nnUNet dir: ", nnunet_dir)

    # Command
    # cmd = [
    #     "/usr/local/bin/nnUNet_predict",
    #     "-i",
    #     str(output_path + input_folder_nnunet),
    #     "-o",
    #     str(output_path + output_folder_nnunet),
    #     "-tr",
    #     "nnUNetTrainerV2",
    #     "-ctr",
    #     "nnUNetTrainerV2CascadeFullRes",
    #     "-m",
    #     "3d_fullres",
    #     "-p" "nnUNetPlansv2.1",
    #     "-t" "Task313_Eye"
    # ]
    cmd1 = ["ls", "-R", "/flywheel"]
    subprocess.call(cmd1)
    # cmd2 = ["find", "/", "-type", "f", "-name", "nnUNet_predict"]
    # subprocess.call(cmd2)
    cmd3 = ["ls", "-R", "/opt/nnunet_resources"]
    subprocess.call(cmd3)
    # cmd4 = ["ls", "-R", "/usr"]
    # subprocess.call(cmd4)

    # log.info(f"Calling...\n{' '.join(cmd)}")

    # process = subprocess.Popen(
    #     cmd, cwd=".", stdout=subprocess.PIPE, stderr=subprocess.PIPE  # cwd="."
    # )


    # Stream the output from p.communicate so the user can monitor the progress continuously.
    # This approach is taken from:
    # https://gitlab.com/flywheel-io/flywheel-apps/nifti-to-dicom/-/blob/0.1.0/fw_gear_nifti_to_dicom/pixelmed.py
    # while True:
    #     time.sleep(5)
    #     if process.poll() is None:
    #         output, _ = process.communicate()
    #         print(output.decode("utf-8").strip() + "\n")
    #     else:
    #         if process.returncode != 0:
    #             log.error(
    #                 f"AEye segmentation failed with exit_code: {process.returncode}"
    #             )
    #             raise SystemExit(1)
    #         else:
    #             log.info("AEye segmentation completed")
    #             # move combined segmentation to the output directory
    #             # shutil.move("/flywheel/v0/output.nii.gz", renamed_path)
    #             subprocess.call(cmd)
    #             sys.exit(process.returncode)


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


def get_nnunet_dir():
    """
    Get the nnUNet directory and sets up nnUNet environment variables.

    Returns:
        str: The path to the nnUNet directory.
    """

    # Get the path to the nnUNet directory
    home_path = Path("/tmp") if str(Path.home()) == "/" else Path.home()
    nnunet_dir = home_path / "usr/local/bin"

    # This variables will only be active during the python script execution. Therefore
    # we do not have to unset them in the end.
    os.environ["nnUNet_raw"] = "/opt/nnunet_resources/nnUNet_raw_data_base"  # not needed, just needs to be an existing directory
    os.environ["nnUNet_preprocessed"] = "/opt/nnunet_resources/nnUNet_preprocessed"  # not needed, just needs to be an existing directory
    os.environ["nnUNet_results"] = "/opt/nnunet_resources/nnUNet_trained_models"

    return nnunet_dir


# Only execute if file is run as main, not when imported bu another module
if __name__ == "__main__":
    # Get access to gear config, inputs and sdk client if enabled
    with GearContext() as gear_context:
        # Initialize logging, set logging level based on `debug` configuration
        gear_context.init_logging()
        # Pass the gear context into main function defined above
        main(gear_context)
