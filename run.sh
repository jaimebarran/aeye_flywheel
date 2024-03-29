#!/usr/bin/env bash 

IMAGE=jaimebarran/fw_gear_aeye:0.0.0

# Command:
sudo docker run --rm --runtime=nvidia --shm-size=10gb -v \
	/mnt/sda1/Repos/flywheel/aeye_flywheel/input:/flywheel/v0/input -v \
	/mnt/sda1/Repos/flywheel/aeye_flywheel/output:/flywheel/v0/output -v \
	/mnt/sda1/Repos/flywheel/aeye_flywheel/work:/flywheel/v0/work -v \
	/mnt/sda1/Repos/flywheel/aeye_flywheel/config.json:/flywheel/v0/config.json -v \
	/mnt/sda1/Repos/flywheel/aeye_flywheel/manifest.json:/flywheel/v0/manifest.json \
	--entrypoint=/bin/sh -e FLYWHEEL=/flywheel/v0 -e NPP_VERSION=12.2.3.2 -e SHELL=/bin/bash \
	-e NVIDIA_VISIBLE_DEVICES=all -e DALI_BUILD=12152788 -e CUSOLVER_VERSION=11.5.4.101 -e \
	CUBLAS_VERSION=12.3.4.1 -e CUFFT_VERSION=11.0.12.1 -e NVIDIA_REQUIRE_CUDA="cuda>=12.0" -e \
	CUDA_CACHE_DISABLE=1 -e TENSORBOARD_PORT=6006 -e TORCH_CUDA_ARCH_LIST="5.2 6.0 6.1 7.0 \
	7.2 7.5 8.0 8.6 8.7 9.0+PTX" -e NCCL_VERSION=2.19.stable.20231214+cuda12.3 -e \
	CUSPARSE_VERSION=12.2.0.103 -e ENV=/etc/shinit_v2 -e PWD=/flywheel/v0 -e \
	OPENUCX_VERSION=1.15.0 -e NSIGHT_SYSTEMS_VERSION=2023.4.1.97 -e \
	NVIDIA_DRIVER_CAPABILITIES=compute,utility,video -e POLYGRAPHY_VERSION=0.49.4 -e \
	UCC_CL_BASIC_TLS=^sharp -e TRT_VERSION=8.6.3.1+cuda12.2.2.009 -e \
	NVIDIA_PRODUCT_NAME=PyTorch -e RDMACORE_VERSION=39.0 -e COCOAPI_VERSION=2.0+nv0.8.0 -e \
	CUDA_VERSION=12.3.2.001 -e PYTORCH_VERSION=2.3.0a0+ebedce2 -e CURAND_VERSION=10.3.4.107 \
	-e PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python -e PYTORCH_BUILD_NUMBER=0 -e \
	USE_EXPERIMENTAL_CUDNN_V8_API=1 -e CUTENSOR_VERSION=2.0.0.7 -e PIP_DEFAULT_TIMEOUT=100 \
	-e NVFUSER_BUILD_VERSION=d0bb811 -e HPCX_VERSION=2.16rc4 -e TORCH_CUDNN_V8_API_ENABLED=1 \
	-e NVM_DIR=/usr/local/nvm -e GDRCOPY_VERSION=2.3 -e NVFUSER_VERSION=d0bb811 -e \
	OPENMPI_VERSION=4.1.5rc2 -e NVJPEG_VERSION=12.3.0.81 -e \
	LIBRARY_PATH=/usr/local/cuda/lib64/stubs: -e PYTHONIOENCODING=utf-8 -e SHLVL=0 -e \
	BASH_ENV=/etc/bash.bashrc -e CUDNN_VERSION=9.0.0.306 -e \
	NSIGHT_COMPUTE_VERSION=2023.3.1.1 -e DALI_VERSION=1.34.0 -e JUPYTER_PORT=8888 -e \
	PYTORCH_HOME=/opt/pytorch/pytorch -e \
	LD_LIBRARY_PATH=/usr/local/lib/python3.10/dist-packages/torch/lib:/usr/local/lib/python3.10/dist-packages/torch_tensorrt/lib:/usr/local/cuda/compat/lib:/usr/local/nvidia/lib:/usr/local/nvidia/lib64 \
	-e NVIDIA_BUILD_ID=82611821 -e OMPI_MCA_coll_hcoll_enable=0 -e \
	OPAL_PREFIX=/opt/hpcx/ompi -e CUDA_DRIVER_VERSION=545.23.08 -e LC_ALL=C.UTF-8 -e \
	TRANSFORMER_ENGINE_VERSION=1.3 -e PYTORCH_BUILD_VERSION=2.3.0a0+ebedce2 -e \
	_CUDA_COMPAT_PATH=/usr/local/cuda/compat -e CUDA_HOME=/usr/local/cuda -e \
	CUDA_MODULE_LOADING=LAZY -e \
	PATH=/usr/local/lib/python3.10/dist-packages/torch_tensorrt/bin:/usr/local/mpi/bin:/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/ucx/bin:/opt/tensorrt/bin \
	-e MOFED_VERSION=5.4-rdmacore39.0 -e NVIDIA_PYTORCH_VERSION=24.02 -e \
	TRTOSS_VERSION=23.11 -e TORCH_ALLOW_TF32_CUBLAS_OVERRIDE=1 -e _=/usr/bin/printenv -e \
	nnUNet_raw_data_base=/opt/nnunet_resources/nnUNet_raw_data_base -e \
	nnUNet_preprocessed=/opt/nnunet_resources/nnUNet_preprocessed -e \
	RESULTS_FOLDER=/opt/nnunet_resources/nnUNet_trained_models \
	$IMAGE -c "python run.py" \
