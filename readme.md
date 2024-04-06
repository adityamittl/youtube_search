# YouSync

>  API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

Design methodology:

Application create a celery beats of 10 seconds that fetch videos from the youtube and saved into the database, storing only unique data and discard already existing video metadata

## Steps to run

create a ```.env``` file containing

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

# start celery workers
celery -A youtube_search worker -E --loglevel=INFO --without-gossip --without-mingle --without-heartbeat -Ofair

# enable heart beat
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

**Role of slave nodes [With kubernetes]** : 
Slave nodes are the user interacting nodes whoch serves the api to the end user to fetch the new metadatas, it can be scalable with the cpu/memory or traffic (Use of KEDA with prometheus metrics) this will scale and populate new pods(application container run inside pods) based on the policy in new node pools (may be in the same region or different availablity zone)

**Increase Efficiency** : 
Caching should be done on top 100 results every time, because we are paginating responsed by the fractio of 10 (as of now in this application), use redis of memcache for the same to resuce the db io operations which will drop the response time.
> to achieve this, we can establish a kafka or jenkins pipeline to ingest new data from the master node to every slave nodes's redis client, maintaining redis in every node is a good option as it will not bottleneck one pod or server, also if any zone goes down, the response time will still remains the same.

**Production setup** :
for production setup, the master node (which is fetching meta data) should not be exposed to the public network, (Internal DNS resolution) and for slave node, traffic ingress policy should be like -

_Nginx ->  Gunicorn -> WSGI django application_

NGINX will act as reverse proxy and load balancer protecting internal ips from public infrastructure.


## Application Screenshots 

| ![image](https://github.com/adityamittl/youtube_search/assets/76921082/267d5418-67c5-41f9-a825-7a468e1665e2) |
|:--:|
| Fig 1. Video Meta data Fetch Status |

| ![image](https://github.com/adityamittl/youtube_search/assets/76921082/ac9d5851-22bc-4cbd-ad2e-863d8a52cd99) |
|:--:|
| Fig 2. Application Dashboard |

 | ![image](https://github.com/adityamittl/youtube_search/assets/76921082/7757764d-0419-4433-a77d-2e151e528599) |
 |:--:|
 | Fig 3. Application Dashboard including pagination |

 ### Observability Dashboard
 ![image](https://github.com/adityamittl/youtube_search/assets/76921082/78bd3f29-aa8a-4f0a-94ec-2fc8482d5530)

![image](https://github.com/adityamittl/youtube_search/assets/76921082/c6725a98-b6ba-415a-94e8-f29bd67c68a9)

### Admin DB Snapshot
![image](https://github.com/adityamittl/youtube_search/assets/76921082/8cd796d9-b5ca-4e42-92c2-0d09f3b2a0ab)

## Tech-Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)
