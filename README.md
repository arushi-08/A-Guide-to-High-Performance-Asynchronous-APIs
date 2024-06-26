# A Guide to High Performance Asynchronous APIs

A guide to developing a robust web application capable of handling batch processing tasks through asynchronous calls, following the Publisher-Subscriber design pattern. The application leverages the highly-essential tools to get the ground running for efficient and scalable processing of large datasets. \
Key Features: \
Asynchronous Task Execution: Utilize Celery, a powerful distributed task queue, to offload time-consuming batch processing tasks from the main application thread, ensuring responsiveness and optimal performance.

Publisher-Subscriber Pattern: Implement a decoupled architecture by adopting the Publisher-Subscriber design pattern, enabling seamless communication between different components of the system.

Reliable Message Queueing: Leverage Redis, an in-memory data structure store, as a reliable and high-performance message broker for efficient task distribution and management.

Persistent Data Storage: Integrate MongoDB, a flexible and scalable NoSQL database, to store and retrieve processed data, ensuring data integrity and enabling efficient querying.

Containerized Deployment: Package the entire application stack using Docker containers, facilitating consistent and reproducible deployments across different environments, from development to production.


**Technologies Used** \
Celery: robust and efficient distributed task queue system.

Redis: in-memory data structure store.

MongoDB: scalable NoSQL database.

Docker: consistent and reproducible deployments across different environments.


## Docker setup
### Build and start the docker containers
`docker compose -up d`

### Start Application:
`python app.py`


