# The Event Bus implementation with RabbitMQ and Python

## Ideation
Basic functionality achieved already in this forked repository.
I want to improve on it by implementing more UI for customizability
1. Visualise publisher sending event
2. Visualise event routing in event bus
3. UI to add more new queues 
4. UI to add more different type of events

## User Journey
As a developer
1. Request for an Event Bus - SDC provisions an Event Bus with endpoints and login credentials
2. Login and access Event Bus, create specific queues with filters intended
3. Send test event to check if queues work as intended
4. Connect new queues to endpoint of microservice *(open firewalls)*
5. Connect event publisher to Event Bus *(open firewalls)*

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




