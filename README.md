# Flask example: Ticket system

## Introduction

Sample api on a simple ticket system using flask.

## Requirements

- Python 3.7+
- Flask 1.1.4

## Installation

### Local

Create a virtual environment and install dependencies:

```
python3.7 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Docker

Create the docker image. This step generates the image that will be used to create the container. In addition, the application and all its dependencies are installed:

```
docker build -t flask-ticket:latest .
```

Once this step is ready, run the container:

```
docker run -it -p 5000:5000 --rm --name flask-ticket-example flask-ticket:latest
```

The _--rm_ option is to remove the container once its execution stops.

### Run tests

Use unitTest for testing:

```
python -m unittest
```

## Author

* **Juan Carlos Ramos Peroni** - Developer - [peronidev](https://bitbucket.org/peronidev)
