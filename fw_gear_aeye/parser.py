"""Parser module to parse gear config.json"""
# from pathlib import Path
from typing import Tuple

from flywheel import GearContext
# from flywheel_gear_toolkit import GearToolkitContext

import os
import logging
# import json

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
    print("Config measurement: ", config_measurement)
    print("Debug: ", config_debug)

    # Get input file
    input_file = gear_context.get_input_path('nifti')
    print("Input file: ", input_file)

    # Determine measurement
    # Check if autodetect, otherwise use config.json/manifest.json
    if config_measurement == 'auto-detect':

        # # Get measurement from context
        # with open(CONFIG_FILE, 'r') as f:
        #     config_data = json.load(f)
        #     intent = config_data['inputs']['nifti']['object']['classification']['Intent'][0]
        #     pprint(intent)
        #     measurement = config_data['inputs']['nifti']['object']['classification']['Measurement'][0]
        #     pprint(measurement)

        # Get measurement from context
        intent = gear_context.get_input('nifti')['object']['classification']['Intent']
        print("Intent: ", intent)
        measurement = gear_context.get_input('nifti')['object']['classification']['Measurement']
        print("Measurement: ", measurement)
        modality = gear_context.get_input('nifti')['object']['modality']
        print("Modality: ", modality)

        # {
        # 'base': 'file',
        # 'hierarchy': {'id': 'aex', 'type': 'acquisition'},
        # 'location': {'name': 'I_Kopf_t1_mpr_tra_iso_p2.nii.gz',
        #             'path': '/flywheel/v0/input/nifti/I_Kopf_t1_mpr_tra_iso_p2.nii.gz'},
        # 'object': {'classification': {'Intent': [], 'Measurement': []},
        #             'info': {},
        #             'measurements': [],
        #             'mimetype': '',
        #             'modality': '',
        #             'size': 8703369,
        #             'tags': [],
        #             'type': ''}
        # }

        if intent == 'Functional':
            config_measurement = 'functional'
        elif intent == 'Structural':
            if measurement == 'T1':
                config_measurement = 't1'
            elif measurement == 'T2':
                config_measurement = 't2'

    return input_file, config_measurement, config_debug
