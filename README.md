rest-battles
============

Example Flask app for best practices practice. We talkin' about practice?

I'm very familiar with Django and Ansible,
built this example app to help broaden my horizons slightly
- Flask, SQLAlchemy, Docker, Python3, ... Packer ...

You have to have python3 installed.

Once you have an environment with the correct python and pip on your PATH, you can:

    pip install -r requirements.txt

Run the tests against sqlite in memory:

    ./test.sh
    
Find the test coverage report in the htmlcov directory (100%).
    
Build a single docker image that runs Postgres and Flask (WIP):

    sudo docker build .

Still working with how to provision the image.
May mix in packer to use ansible to build the docker image.
Currently, we have a pure Dockerfile which doesn't quite configure PG correctly.
