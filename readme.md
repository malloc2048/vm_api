# LibVirt REST API
A simple REST API to interact with libvirt for VM information and control.  
<b>THIS IS A DEVELOPMENT PROJECT AND NOT SUITABLE FOR PRODUCTION ENVIRONMENTS </b>

## Structure
```
├── api
│   ├── api.py
│   ├── gunicorn.conf.py
│   ├── __init__.py
│   └── utils.py
├── Dockerfile
├── packages.list
├── Pipfile
├── Pipfile.lock
├── README.md
└── scripts
    ├── build_image.sh
    ├── run_local.sh
    └── start.sh
```

## Running the API
The ```scripts``` directory contains some convenience scripts used during development to build the docker container and to run 

### build_image.sh
This script will build the API docker image and install the Flask app source code and start script  
Note that all dependencies for the base docker system and the python environment should be installed during image build.

### run_local.sh
This script will run the docker image built with ```build_image.sh``` 

If no arguments are provided the gunicorn server will start automatically.  

If an argument is provided the command in the argument will replace the container entry point and attempt to be run  
During development ```bash``` was used as an argument to get a shell into the container  

## API Swagger documentation
There is swagger based documentation available to try out the API at the root of the server.  
Currently the gunicorn server will bind to ```0.0.0.0:8001``` so the swagger docs are available at localhost:8001 on the  
host running the docker container.

## Future enhancements
There are some improvements that could be made to this project if I get the time.
* bind to a specific IP address determined by the looking for a specific interface (a VPN interface for example)
* make the API token more robust and not a single hard coded 
* add support for connecting to a remote qemu/libvirt host instead of the docker host.
