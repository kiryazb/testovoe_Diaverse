#!/bin/bash

cd src

if [[ "${1}" == "celery" ]]; then
  celery --app=ReservationSystem.utils:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
  celery --app=ReservationSystem.utils:celery flower
 fi