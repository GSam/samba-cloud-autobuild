FROM ubuntu:14.04

RUN apt-get update -y && \
  DEBIAN_FRONTEND=noninteractive \
  apt-get -yq install \
  {% for item in packages %}
  {{ item }} \
  {% endfor %}
  && apt-get -y clean
