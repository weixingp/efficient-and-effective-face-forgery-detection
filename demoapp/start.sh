#!/bin/bash

exec python ./app.py &
exec flask --app webserver run