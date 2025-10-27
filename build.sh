#!/bin/bash
# Build script to force clean installation
pip uninstall -y psycopg2 psycopg2-binary psycopg || true
pip cache purge || true
pip install --no-cache-dir --force-reinstall psycopg2-binary==2.9.5
pip install --no-cache-dir -r requirements.txt