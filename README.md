The applications are divided into two parts:
backend
frontend

Most scripts are launched from the root project.

Make sure docker-compose is installed:
https://docs.docker.com/compose/install/

After docker is installed run the script:
./ci/up_dev.sh

When completed, navigate to the following to get
respective sides:
BACKEND http://localhost:5000/openapi/
FRONTEND http://localhost:3000

To shut down the application:
./ci/down_dev.sh
