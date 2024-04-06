# YouSync

>  API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

Design methodology:

Application create a celery beats of 10 seconds that fetch videos from the youtube and saved into the database, 

storing only unique data and discard already existing video metadata

Steps to run

create a .env file containing

```
YOUTUBE_KEY =
REDIS_BROKER =
```

To run application follow steps

```shell
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate

# If install redis client locally easy method is to run it in docker file
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest

#start celery workers
celery -A youtube_search worker --loglevel=INFO --without-gossip --without-mingle --without-heartbeat -Ofair

#enable heart beat
celery -A youtube_search beat --loglevel=info

# If task observability
celery -A youtube_search flower --port=5555
```

## Scalability 

**we can further scale the application using kubernetes**

### Howto
The scalable architecture should have a master node and multiple child nodes

**Role of master node** 
Master node will be responsible for fetching metadata form the google servers, since it is supposed to be interacting with only one client, it one node should be good enough 

**Role of slave nodes [With kubernetes]**
Slave nodes are the user interacting nodes whoch serves the api to the end user to fetch the new metadatas, it can be scalable with the cpu/memory or traffic (Use of KEDA with prometheus metrics) this will scale and populate new pods(application container run inside pods) based on the policy in new node pools (may be in the same region or different availablity zone)

**Increase Efficiency**
Caching should be done on top 100 results every time, because we are paginating responsed by the fractio of 10 (as of now in this application), use redis of memcache for the same to resuce the db io operations which will drop the response time.
> to achieve this, we can establish a kafka or jenkins pipeline to ingest new data from the master node to every slave nodes's redis client, maintaining redis in every node is a good option as it will not bottleneck one pod or server, also if any zone goes down, the response time will still remains the same.

**Production setup** 
for production setup, the master node (which is fetching meta data) should not be exposed to the public network, (Internal DNS resolution) and for slave node, traffic ingress policy should be like -

Nginx ->  Gunicorn -> WSGI django application 

NGINX will act as reverse proxy and load balancer protecting internal ips from public infrastructure.

## Application Screenshots 

