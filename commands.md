# Useful commands

## Docker

- Build docker image

`docker build --no-cache -t jaimebarran/fw_gear_aeye_test .`

- Push docker image

`docker push jaimebarran/fw_gear_aeye_test`

- Run docker image interactively (local image)

`docker run -it --rm docker.io/jaimebarran/fw_gear_aeye_interactive /bin/bash`

- Run docker image interactively (remote image)

`docker run -it --rm jaimebarran/fw_gear_aeye_interactive /bin/bash`

- List images

`docker images` or `docker image ls`

- List containers
`docker ps -a` or `docker container ls -a`

- Remove image

`docker rmi <image_id>`

- Remove container

`docker rm <container_id>`

- Prune images

`docker image prune`

- Prune containers

`docker container prune`

## Flywheel

- Log in

`fw login {FW_API_KEY}`

- Test local gear

`fw gear local --nifti=I_Kopf_t1_mpr_tra_iso_p2.nii.gz --measurement="auto-detect" --debug=true`

- Upload gear

`fw gear upload`

### Flywheel beta

- Log in

`fw-beta login --api-key=${FW_API_KEY}`

## nnUNet

- Test to see if it is installed

`nnUNet_predict -h`

- Run nnUNet locally

        `nnUNet_predict -i "/mnt/sda1/Repos/flywheel/aeye_flywheel/output/input" -o "/mnt/sda1/Repos/flywheel/aeye_flywheel/output/output" -tr nnUNetTrainerV2 -ctr nnUNetTrainerV2CascadeFullRes -m 3d_fullres -p nnUNetPlansv2.1 -t Task313_Eye`

- Run nnUNet through Docker pushed image

        `docker run --rm --gpus device=0 --shm-size=10gb -v /home/jaimebarranco/Desktop/nnUNet:/opt/nnunet_resources jaimebarran/fw_gear_aeye_interactive:latest nnUNet_predict -i /opt/nnunet_resources/nnUNet_inference/input -o /opt/nnunet_resources/nnUNet_inference/output -tr nnUNetTrainerV2 -ctr nnUNetTrainerV2CascadeFullRes -m 3d_fullres -p nnUNetPlansv2.1 -t Task313_Eye`

- Run nnUNet through Docker pushed image with trained model

        `docker run --rm --gpus device=0 --shm-size=10gb -v /home/jaimebarranco/Desktop/nnUNet:/opt/nnunet_resources jaimebarran/fw_gear_aeye_interactive:latest nnUNet_predict -i /opt/nnunet_resources/nnUNet_inference/input -o /opt/nnunet_resources/nnUNet_inference/output -tr nnUNetTrainerV2 -ctr nnUNetTrainerV2CascadeFullRes -m 3d_fullres -p nnUNetPlansv2.1 -t Task313_Eye`

- Export environment variables (required)

  - nnUNet_raw

    `export nnUNet_raw="/home/jaimebarranco/Desktop/nnUNet/nnUNet_raw_data"`

  - nnUNet_preprocessed

    `export nnUNet_preprocessed="/home/jaimebarranco/Desktop/nnUNet/nnUNet_preprocessed"`

  - nnUNet_results

    `export nnUNet_results="/home/jaimebarranco/Desktop/nnUNet/nnUNet_trained_models"`

## File permissions

- Change file permissions

    `sudo chmod -R a+rw /mnt/sda1/Repos/flywheel/aeye_flywheel/output/input/`

- Change file owner

    `sudo chown jaimebarranco output/input/I_Kopf_t1_mpr_tra_iso_p2.nii.gz`
