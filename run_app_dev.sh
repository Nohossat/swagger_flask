#!/bin/bash
flask init-db | flask run --host=0.0.0.0 --port=$FLASK_PORT