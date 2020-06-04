# Game Service

Responsible for

## Development

First start a virtual environment. For example:

> python3 -m venv venv
> . venv/bin/activate

Then install the dependencies with `pip install -r requirements`.

Run `make up`. You may have to wait until the MySQL instance comes up before
the other containers will stay alive. To check whether the MySQL database has
finished coming up, run `docker logs risk-db` and look for text similar to
`ready for connections. Version: '8.0.20'  socket:
'/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.`. Once
the MySQL container has finished coming up run `make up` again. You can check
that all expected containers are up by running `docker ps`.
 
## Using the API 

### GET `/v0/lookup/`

``` http 
    curl localhost:8000/v0
```
