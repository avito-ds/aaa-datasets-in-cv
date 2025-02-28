FROM nvcr.io/nvidia/pytorch:23.10-py3

WORKDIR /app

RUN pip uninstall poetry -y
RUN pip uninstall poetry-core -y

RUN pip install -U pip poetry==1.6.1 poetry-core==1.7.0

COPY jupyter_notebook_config.py /root/.jupyter/

# RUN apt install \
#     libsoxr0 \
#      libopus0 \
#      libwebpmux3 \
#      libswresample3 \
#      libwebpdemux2 \
#      libva \
#     -x11-2 libxcb \
#     -render0 libzmq5 \
#      libva \
#     -drm2 libx264 \
#     -160 libchromaprint1 \
#      libavformat58 \
#      libatlas3 \
#     -base libvorbis0a \
#      libsodium23 \
#      libsnappy1v5 \
#      libvdpau1 \
#      libzvbi0 \
#      libdatrie1 \
#      libavutil56 \
#      libbluray2 \
#      libpgm \
#     -5.3-0 libxvidcore4 \
#      libopenmpt0 \
#      libvorbisfile3 \
#      libvpx6 \
#      libgdk \
#     -pixbuf-2.0-0 libavcodec58 \
#      libgme0 \
#      libtheora0 \
#      libswscale5 \
#      libpangoft2 \
#     -1.0-0 libxcb \
#     -shm0 libshine3 \
#      libwavpack1 \
#      libcairo \
#     -gobject2 libmpg123 \
#     -0 libudfread0 \
#      libsrt1 \
#     .4-gnutls libtwolame0 \
#      libdrm2 \
#      libgfortran5 \
#      libxfixes3 \
#      ocl-icd-libopencl1 \
#      libx265 \
#     -192 libopenjp2 \
#     -7 librsvg2 \
#     -2 libaom0 \
#      libva2 \
#      libpixman \
#     -1-0 libthai0 \
#      libmp3lame0 \
#      libnorm1 \
#      libharfbuzz0b \
#      libssh \
#     -gcrypt-4 libdav1d4 \
#      libogg0 \
#      libgraphite2 \
#     -3 librabbitmq4 \
#      libpango \
#     -1.0-0 libvorbisenc2 \
#      libopenblas0 \
#     -pthread libcodec2 \
#     -0.9 libgsm1 \
#      libcairo2 \
#      libspeex1 \
#      libxrender1 \
#      libpangocairo \
#     -1.0-0

COPY . $PROJECT_ROOT

RUN poetry config virtualenvs.create false
RUN poetry update
RUN poetry install

RUN python -c "from opencv_fixer import AutoFix; AutoFix()"