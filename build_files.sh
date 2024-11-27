#!/bin/bash
echo "Collecting static files"
python3 manage.py collectstatic --noinput
mkdir -p staticfiles_build
cp -r staticfiles/* staticfiles_build/
