#!/bin/sh

docker exec -it `docker ps --format  "{{.ID}}"` /bin/sh
