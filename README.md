# Pytea

[Gitea API](https://try.gitea.io/api/swagger) wrapper for Python (3 only).


## Install

### From sources

    python setup.py install


### With Pip

    pip install git+https://github.com/arount/pytea


## Basic usage


    import pytea

	api = pytea.API('http://192.168.100.10:3000')
	api.get('/version')
	api.get('/orgs/an-organisation/members')


### Authentification token


Setup authentification token:

    import pytea
	api = pytea.API('http://192.168.100.10:3000', token="AUTH-TOKEN")
	api.delete('/admin/users/arount')


### Main API methods


    api.get('route')   # Send GET query to route
	api.post('route')  # Send POST query to route
	api.patch('route') # Send PATCH query to route
	api.put('route')   # Send PUT query to route


### Alternative API method


	# Send GET query to route with parameters
    api.call('route', method='get', params={"body": "Egg, bacon, sausages and SPAM")


## Exceptions


Exceptions are raised before sending query. If API respond error message no exception will be raised (for the moment, at least)


### Authentification token


If auth token is not set when you are trying to access to a protected resource:

	api = pytea.API('http://192.168.100.10:3000')
	api.delete('/admin/users/arount')


    pytea.PyteaRequestException: Resource '/admin/users/{username}' require an authentification token.


### Resource do not exists


    api.get('/fake/route')


	pytea.PyteaRequestException: Path '/fake/route' did not match with any resource


### Method do not exists for resource


	api.delete('/markdown')


	pytea.PyteaRequestException: Resource '/markdown' did not expect method DELETE

