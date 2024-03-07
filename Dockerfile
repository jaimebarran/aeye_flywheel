FROM alpine:latest

RUN apk add --no-cache bash \
    --update \
    python3 \
    py-pip \
    # && apt-get update -y \
    && pip install flywheel-sdk --break-system-packages \
    # && apt-get clean \
    && rm -rf /var/cache/apk/*

ENV FLYWHEEL="/flywheel/v0"
WORKDIR ${FLYWHEEL}

# Installing main dependencies
COPY requirements.txt ${FLYWHEEL}/requirements.txt
# RUN pip install --no-cache-dir -r $FLYWHEEL/requirements.txt

# Installing the current project (most likely to change, above layer can be cached)
COPY fw_gear_aeye ${FLYWHEEL}/fw_gear_aeye
COPY run.py ${FLYWHEEL}/run.py
COPY manifest.json ${FLYWHEEL}/manifest.json
COPY README.md ${FLYWHEEL}/README.md

# Configure entrypoint
RUN chmod a+x ${FLYWHEEL}/run.py
ENTRYPOINT ["python","/flywheel/v0/run.py"]

# build docker image
# docker build --no-cache -t jaimebarran/fw_gear_aeye_test .

# push docker image
# docker push jaimebarran/fw_gear_aeye_test

# test locally
# fw gear local --nifti=I_Kopf_t1_mpr_tra_iso_p2.nii.gz --measurement="auto-detect" --debug=true