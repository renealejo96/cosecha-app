#!/bin/bash
# Build script to force clean installation
pip uninstall -y psycopg2 psycopg2-binary || true
pip cache purge || true
pip install --no-cache-dir -r requirements.txt