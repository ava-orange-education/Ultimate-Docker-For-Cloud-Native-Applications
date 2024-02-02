# TLS Encrypted Authentication in Docker Daemon

## Pre-requisites

Install the following tools:

- [Docker](https://docs.docker.com/install/)
- [Just](https://github.com/casey/just/#installation)
- [OpenSSL](https://www.openssl.org/) or [Step CLI](https://smallstep.com/docs/step-cli/)

## Generate the certificates

```bash
just generate-certificates-openssl
# or
just generate-certificates-step
```

## Run the Docker Daemon

```bash
just run-dockerd
```
