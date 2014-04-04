pysheet
=======

spreadsheets for engineers


To start the web-service:
```bash
cd <git-repository>/pysheet
gunicorn server:app -w 8 --max-requests 1
# each server thread only stays alive for one request, so that the new code is loaded
# from the Tables.
```
