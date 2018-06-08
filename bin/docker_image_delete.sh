#!/bin/bash

select x in `docker images --format '{{.ID}}--{{.Repository}}/{{.Tag}}'` ; do docker rmi `echo $x | awk -F'--' '{print $1}'`; done
