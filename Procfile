release: chmod +x build.sh && ./build.sh
web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app