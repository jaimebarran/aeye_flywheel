"""Parser module to parse gear config.json"""
# from pathlib import Path
from typing import Tuple

from flywheel import GearContext
# from flywheel_gear_toolkit import GearToolkitContext

import os
import json

# DEFINE VARIABLES
FLYWHEEL_BASE = "/flywheel/v0"
MANIFEST_FILE = os.path.join(FLYWHEEL_BASE, "manifest.json")
CONFIG_FILE = os.path.join(FLYWHEEL_BASE, "config.json")
INPUT_DIR = os.path.join(FLYWHEEL_BASE, "input", "nifti")
ROOTOUT_DIR = os.path.join(FLYWHEEL_BASE, "output")
OUTPUT_DIR = os.path.join(ROOTOUT_DIR, "out")
WORKING_DIR = os.path.join(ROOTOUT_DIR, "work")
# CONTAINER = '[flywheel/aeye]'


# This function mainly parses gear_context's config.json file
# and returns relevant inputs and options.


def parse_config(
    gear_context: GearContext,
) -> Tuple[str, str]:
    """Measurement, and outputs"""

    # Get config settings
    config_measurement = gear_context.config['measurement']
    config_debug = gear_context.config['debug']
    print(f"measurement: {config_measurement}")
    print(f"debug: {config_debug}")

    # Determine measurement
    # Check if autodetect, otherwise use config.json/manifest.json
    if config_measurement == 'auto-detect':

        # Get measurement from context
        with open(CONFIG_FILE, 'r') as f:
            config_data = json.load(f)
            intent = config_data['inputs']['nifti']['object']['classification']['Intent'][0]
            measurement = config_data['inputs']['nifti']['object']['classification']['Measurement'][0]

        if intent == 'Functional':
            config_measurement = 'functional'
        elif intent == 'Structural':
            if measurement == 'T1':
                config_measurement = 't1'
            elif measurement == 'T2':
                config_measurement = 't2'

    input_file = gear_context.get_input_path('nifti')
    print(f"input: {input_file}")

    # # Get input_file
    # # Find input file in input directory with the extension .nii, .nii.gz
    # input_file = [
    #     f for f in os.listdir(INPUT_DIR) if f.endswith((".nii", ".nii.gz"))
    # ]

    # # If input file not found, raise error
    # if not input_file:
    #     print(
    #         f"No Nifti files (.nii or .nii.gz) were found \
    #         within input directory {INPUT_DIR}"
    #     )
    #     exit(17)

    return input_file, config_measurement, config_debug
