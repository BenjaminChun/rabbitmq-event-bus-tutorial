# The Event Bus implementation with RabbitMQ and Python

## Installation

Requires python 3+, pip and docker compose (optionally).

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




