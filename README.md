# SupportOps OpenEnv

## Description
Simulates real-world customer support workflow.

## Tasks
- easy: refund
- medium: urgent technical
- hard: multi-intent escalation

## Run
docker build -t support-env .
docker run support-env

## Env Variables
HF_TOKEN=
API_BASE_URL=
MODEL_NAME=# MyOpenEnv
