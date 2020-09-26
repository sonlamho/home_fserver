#!/bin/bash
export FLASK_APP=home_fserver && export FLASK_ENV=production && uwsgi --socket 0.0.0.0:58000 --master --protocol=http -w wsgi:app --processes 6 --threads 2
