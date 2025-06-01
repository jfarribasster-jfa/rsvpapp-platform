#!/bin/bash

set -e

# The exec command is used in order to avoid creating a new process,
# which ensures any signals (such as SIGTERM ) are recieved by our uwsgi process rather than being swallowed by the parent process.
exec uwsgi --http 0.0.0.0:5000 --wsgi-file /app/rsvp.py --callable app --stats 0.0.0.0:5001
