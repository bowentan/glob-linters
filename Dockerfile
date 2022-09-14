FROM python:3.10.7-alpine3.16

LABEL org.opencontainers.image.source https://github.com/bowentan/glob-linters

RUN apk add --no-cache \
    bash=5.1.16-r2 \
    ca-certificates=20220614-r0 \
    cargo=1.60.0-r2 \
    cmake=3.23.1-r0 \
    coreutils=9.1-r0 \
    curl=7.83.1-r3 \
    file=5.41-r0 \
    gcc=11.2.1_git20220219-r2 \
    g++=11.2.1_git20220219-r2 \
    git=2.36.2-r0 \
    git-lfs=3.1.4-r4 \
    gnupg=2.2.35-r4 \
    icu-libs=71.1-r2 \
    libc-dev=0.7.2-r3 \
    libcurl=7.83.1-r3 \
    libffi-dev=3.4.2-r1 \
    libgcc=11.2.1_git20220219-r2 \
    libintl=0.21-r2 \
    libssl1.1=1.1.1q-r0 \
    libstdc++=11.2.1_git20220219-r2 \
    libxml2-dev=2.9.14-r1 \
    libxml2-utils=2.9.14-r1 \
    linux-headers=5.16.7-r1 \
    make=4.3-r0 \
    openssh-client=9.0_p1-r2 \
    openssl-dev=1.1.1q-r0 \
    zlib=1.2.12-r3 \
    zlib-dev=1.2.12-r3

RUN pip install --no-cache-dir glob-linters==0.1.1.20220914135920

ENTRYPOINT [ "glob_linters" ]
