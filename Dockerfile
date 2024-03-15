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

# build docker image
# docker build --no-cache -t jaimebarran/fw_gear_aeye_test .

# push docker image
# docker push jaimebarran/fw_gear_aeye_test

# test locally
# fw gear local --nifti=I_Kopf_t1_mpr_tra_iso_p2.nii.gz --measurement="auto-detect" --debug=true
# sudo chmod -R a+rw /mnt/sda1/Repos/flywheel/aeye_flywheel/output/input/
# sudo chown jaimebarranco output/input/I_Kopf_t1_mpr_tra_iso_p2.nii.gz

# docker run interactively (local image)
# docker run -it --rm docker.io/jaimebarran/fw_gear_aeye_interactive /bin/bash
# docker run interactively (pushed image)
# docker run -it --rm jaimebarran/fw_gear_aeye_interactive /bin/bash

# export nnunet path (bash)
# export PATH=/home/jaimebarranco/miniconda3/envs/a-eye/bin:$PATH

# test nnunet locally without docker
# conda env list
# conda activate a-eye
# nnUNet_predict -h
# export nnUNet_raw_data_base="/home/jaimebarranco/Desktop/nnUNet/nnUNet_raw_data"
# export nnUNet_preprocessed="/home/jaimebarranco/Desktop/nnUNet/nnUNet_preprocessed"
# export RESULTS_FOLDER="/home/jaimebarranco/Desktop/nnUNet/nnUNet_trained_models"
# nnUNet_predict -i "/mnt/sda1/Repos/flywheel/aeye_flywheel/output/input" -o "/mnt/sda1/Repos/flywheel/aeye_flywheel/output/output" -tr nnUNetTrainerV2 -ctr nnUNetTrainerV2CascadeFullRes -m 3d_fullres -p nnUNetPlansv2.1 -t Task313_Eye

# test nnunet from docker image
# docker run --gpus device=0 --shm-size=10gb -v /home/jaimebarranco/Desktop/nnUNet:/opt/nnunet_resources jaimebarran/fw_gear_aeye_interactive:latest nnUNet_predict -i /opt/nnunet_resources/nnUNet_inference/input -o /opt/nnunet_resources/nnUNet_inference/output -tr nnUNetTrainerV2 -ctr nnUNetTrainerV2CascadeFullRes -m 3d_fullres -p nnUNetPlansv2.1 -t Task313_Eye
