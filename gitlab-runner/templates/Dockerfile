FROM ubuntu:14.04
ENV DEBIAN_FRONTEND noninteractive
ENV USER gitlab-runner

RUN locale-gen "en_US.UTF-8" \
    && dpkg-reconfigure locales \
    && useradd -m -s /bin/bash gitlab-runner \
    && echo "gitlab-runner ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/gitlab-runner \
    && apt-get update -y \
    && apt-get -yq install {% for item in packages %}{{ item }} {% endfor %} \
    && apt-get -y clean \
    && apt-get -y autoremove \
    && ln -sf /usr/bin/ld.gold /usr/bin/ld

USER gitlab-runner
WORKDIR /home/gitlab-runner
