#!/bin/bash

select x in `docker images --format '{{.ID}}--{{.Repository}}/{{.Tag}}'` ; do docker rmi "${x%--*}"; done
