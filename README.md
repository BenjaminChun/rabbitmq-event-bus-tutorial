# The Event Bus implementation with RabbitMQ and Python

## Purpose of POC
Demonstrate an example of an application using Event Driven Architecture
Show how users are expected to use event bridge to achieve this
- creation of event bus (header exchanges / any exchange in general)
- creation of queues to host the events
Push effect
- Eventhandler will be in the queue logic which then processes the event
Subscriber
- connects to event bus and creates own queue with own filters
- handles the events in the queue
Publisher
- connects to event bus - creates one if not present
- publishes message

## Ideation
Basic functionality achieved already in this forked repository.
I want to improve on it by implementing more UI for customizability
1. Visualise publisher sending event
2. Visualise event routing in event bus
[x] Subscriber UI to add more new queues - use RabbitMQ UI to add more queues, exchanges etc
[x] Publisher UI to publish different events

## User Journey
As a developer
1. Request for an Event Bus - SDC provisions an Event Bus with endpoints and login credentials
2. Login and access Event Bus, create specific queues with filters intended
3. Send test event to check if queues work as intended
4. Connect new queues to microservice / microservice to connect to event bus and handle events from queue *(open firewalls)*
5. Connect event publisher to Event Bus / publisher microservice to connect to event bus and publish events to event bus *(open firewalls)*

## Requirements
1. python venv 
2. docker compose
3. install python dependencies

## Installation

Requires python 3+, pip and docker compose (optionally).

Set up virtual environment:
```python
python -m venv /path/to/new/virtual/environment # set up virtual env
source <venv>/bin/activate #activate venv
```

Populate .env file:
Copy the .env.example file to create a .env file

Install dependencies:
```shell
pip install -r requirements.txt
```

Run RabbitMQ with docker-compose (or use your own):
```shell
docker compose up -d
```
You can access to RabbitMQ management UI via link - http://localhost:15672 (login: guest, password: guest)

If you want to change default credentials, modify it in the `.env` file.


Start the consumer:
```shell
python src/consumer.py
```

Open a new terminal window and run the producer:
```shell
python3 src/producer.py
```




