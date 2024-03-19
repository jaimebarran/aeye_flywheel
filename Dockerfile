# Template
# Contains pytorch, torchvision, cuda, cudnn
FROM nvcr.io/nvidia/pytorch:24.02-py3

# Mantainer
LABEL maintainer="Jaime Barranco @jaimebarran"

# Install Flywheel
RUN pip install flywheel-sdk --break-system-packages \
    && pip install nnunet
    # && python -c 'import torch;print(torch.__version__)' \
    # && python -c 'import torch;print(torch.backends.cudnn.version())'

# nnUNet dir
ARG resources="/opt/nnunet_resources"
ENV nnUNet_raw_data_base=$resources"/nnUNet_raw_data_base"
ENV nnUNet_preprocessed=$resources"/nnUNet_preprocessed"
ENV RESULTS_FOLDER=$resources"/nnUNet_trained_models"
ENV nnUNet_results=$resources"/nnUNet_trained_models"

# Set environment variables and workdir
ENV FLYWHEEL="/flywheel/v0"
WORKDIR ${FLYWHEEL}

# Installing main dependencies
COPY requirements.txt ${FLYWHEEL}/requirements.txt
RUN pip install --no-cache-dir -r $FLYWHEEL/requirements.txt

# Installing the current project (most likely to change, above layer can be cached)
COPY README.md ${FLYWHEEL}/README.md
COPY manifest.json ${FLYWHEEL}/manifest.json
COPY run.py ${FLYWHEEL}/run.py
COPY fw_gear_aeye ${FLYWHEEL}/fw_gear_aeye
COPY nnUNet/nnUNet_raw_data_base $resources"/nnUNet_raw_data_base"
COPY nnUNet/nnUNet_preprocessed $resources"/nnUNet_preprocessed"
COPY nnUNet/nnUNet_trained_models $resources"/nnUNet_trained_models"

# Configure entrypoint
RUN chmod -R a+rw ${FLYWHEEL}
RUN chmod a+x ${FLYWHEEL}/run.py
ENTRYPOINT ["python3","/flywheel/v0/run.py"]
