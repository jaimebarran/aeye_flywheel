"""Parser module to parse gear config.json"""
from typing import Tuple

from flywheel import GearContext

import os
import logging

log = logging.getLogger(__name__)

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

    # Get input file
    input_file = gear_context.get_input_path('nifti')

    # Determine measurement if auto-detect
    if config_measurement == 'auto-detect':

        # Get measurement from context
        intent = gear_context.get_input('nifti')['object']['classification']['Intent']
        measurement = gear_context.get_input('nifti')['object']['classification']['Measurement']
        modality = gear_context.get_input('nifti')['object']['modality']

        if intent == 'Functional':
            config_measurement = 'functional'
        elif intent == 'Structural':
            if measurement == 'T1':
                config_measurement = 't1'
            elif measurement == 'T2':
                config_measurement = 't2'

    return input_file, config_measurement, config_debug
