---
title: My Open Env
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
---
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
