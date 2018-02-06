# Pytea

[Gitea API](https://try.gitea.io/api/swagger) wrapper for Python (3 only).


## Install

### From sources

    python setup.py install


### With Pip

    pip install git+https://github.com/arount/pytea


## Usage


    import pytea

	api = pytea.API('http://192.168.100.10:3000', token='xxx')
	api.delete('/admin/users/arount')

	api.get('/version')

	api.get('/orgs/an-organisation/members')


