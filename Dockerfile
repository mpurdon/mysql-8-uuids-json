#
# Build Container
#
ARG PYTHON_VERSION=3.7

FROM python:${PYTHON_VERSION}-alpine3.9 as base
ENV PYTHONUNBUFFERED 1

FROM base as mysql_guid_builder

RUN mkdir /install
WORKDIR /install

# install ca-certificates so that HTTPS works consistently
# other runtime dependencies for Python are installed later
RUN apk add --no-cache ca-certificates

RUN apk add --no-cache --upgrade --virtual .build-deps \
            gcc \
            make \
            alpine-sdk \
            libc-dev \
            musl-dev \
            linux-headers \
            pcre-dev \
            python3-dev \
            gettext \
    && apk add --no-cache mysql-dev

COPY requirements.txt /requirements.txt

RUN python3 -m pip install setuptools --upgrade && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade wheel && \
    python3 -m pip install --install-option="--prefix=/install" -r /requirements.txt

#
# Final Container
#
FROM base

COPY --from=mysql_guid_builder /install /usr/local

COPY src /app
WORKDIR /app
