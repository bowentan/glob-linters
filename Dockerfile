FROM python:3.10.7-slim

LABEL org.opencontainers.image.source https://github.com/bowentan/glob-linters

RUN pip install --no-cache-dir glob-linters==0.1.0-alpha.7

ENTRYPOINT [ "glob_linters" ]
