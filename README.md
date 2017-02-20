# SCI-93  

#### That is a simple code for stocks collection from google with Redis

### How to use ?

1. Download redis from https://redis.io/download and startup it.

2. Download SCI-93  
> git clone https://github.com/NGC4258/SCI-93.git  

3. Install python libaries  
> sudo apt install python-pip  
> sudo pip install redis requests  

3. Insert stock number into redis  
> ./src/redis.cli hset 2330 0000-00-00 initial  

4. Start collection  
> python SCI-93  
