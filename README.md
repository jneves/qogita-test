# Global Postal Address Service

Service that records each users postal addresses for anywhere in the world.

# Installation and bootstrapping (developer)

From the directory on which you checked out the repository execute the
following commands:

```
python3 -m venv .ve
. .ve/bin/activate
pip install -r dev_requirements.txt
python manage.py migrate
python manage.py createsuperuser # (example: admin with password password123)
python manage.py runserver
```

API will be accessible on the browser on http://localhost:8000/, you can
login on the top/right corner of the browseable UI.

# Documentation

## Authentication

This API is using token authentication.

Obtain a token from `/auth/v1/login` using the login and password previously created.

Example:

```
$ curl -X POST -u <username>:<password> http://localhost:8000/auth/v1/login
{"token":"7385f45924ac298eb1f0716f66e55942939e2db0"}
```

Then you can use it to access it the authenticated endpoints by using the token
in the Authorization header with a "Token " prefix.

Example:

```
$ curl -X GET --header 'Authorization: Token 7385f45924ac298eb1f0716f66e55942939e2db0' http://localhost:8000/addresses/v1/
{"count":0,"next":null,"previous":null,"results":[]}
```

You can disable the current token in `/auth/v1/logout` or all the current user tokens in `/auth/v1/logout-all`.

Examples:

```
$ curl -X POST --header 'Authorization: Token 7385f45924ac298eb1f0716f66e55942939e2db0' http://localhost:8000/auth/v1/logout
{}
```

```
$ curl -X POST --header 'Authorization: Token 7385f45924ac298eb1f0716f66e55942939e2db0' http://localhost:8000/auth/v1/logout-all
{}
```

Session authentication is enabled to support the browseable API only. Do
NOT try to use it for API access.

## Endpoints

- GET `/` - just a set of links so it's discoverable.

- GET `/addresses/v1/` - paginated list of addresses for the current user.
- POST `/addresses/v1/` - create one or more addresses.
- GET `/addresses/v1/{id}/` - show the content of the address identified by `{id}`.
- PUT `/addresses/v1/{id}/` - change all the values of the address identified by `{id}`.
- PATCH `/addresses/v1/{id}/` - change one or more fields of the address identified by `{id}`.
- DELETE `/addresses/v1/{id}/` - delete the address identified by `{id}`.

- POST `/auth/v1/login` - obtain a new token for the current user.
- POST `/auth/v1/logout` - disable the current token.
- POST `/auth/v1/logout-all` - disable all tokens for the current user.

## Data

The data format is a re-use of the one used by the google-i18n-address package
(which gets it from the Google repository).


| Field  | Type | Description |
| ------------- | ------------- | ------------- |
| country_code | str | 2-letter ISO 3166 code for the country. |
| country_area | str | Country sub-division (state in the US). |
| city | str | City. |
| city_area | str | Sub-division of a city. |
| street_address | str | Street address. |
| postal_code | str | Postal code. |
| sorting_code | str | Sorting code (when relevant). |

The country_code is always mandatory. The others will depend on the country_code
value.

On the API, the data is represented by a JSON dictionary with these fields.
Responses will also have the read-only `id` and `url` fields which represent
the addresses' identifier and the URL to fetch the specific information.

## Examples

### Read the list of addresses

```
$ curl -X GET --header 'Authorization: Token 7385f45924ac298eb1f0716f66e55942939e2db0' http://localhost:8000/addresses/v1/
{"count":0,"next":null,"previous":null,"results":[]}
```

The result is paginated, each page with 10 addresses. You can access a specific page X by adding `?page=X` to the URL.

### Create an address

Validation error (status code 400)

```
$ curl -X POST -H 'accept: application/json'   -H 'Content-Type: application/json' -H 'Authorization: Token 7385f45924ac298eb1f0716f66e55942939e2db0' -d '{"country_code": "US"}' http://localhost:8000/addresses/v1/
{"non_field_errors":["Address failed to validate: country_area: required; city: required; postal_code: required; street_address: required."]}
```

Successful request (status code 200)

```
$ curl -X POST -H 'accept: application/json'   -H 'Content-Type: application/json' -H 'Authorization: Token 7385f45924ac298eb1f0716f66e55942939e2db0' -d '{"country_code": "PT", "city": "Lisboa", "postal_code": "1000-001", "street_address": "Av. Roma, 12 - 2 Dto"}' http://localhost:8000/addresses/v1/
{"url":"http://localhost:8000/addresses/v1/b14f4578-acf1-493e-b138-f05309af6ed7/","id":"b14f4578-acf1-493e-b138-f05309af6ed7","country_code":"PT","country_area":"","city":"LISBOA","city_area":"","street_address":"Av. Roma, 12 - 2 Dto","postal_code":"1000-001","sorting_code":"","owner":1}
```

### Create multiple addresses

Successful request (status code 200)

```
$ curl -X POST -H 'accept: application/json'   -H 'Content-Type: application/json' -H 'Authorization: Token 7385f45924ac298eb1f0716f66e55942939e2db0' -d '[{"country_code": "PT", "city": "Lisboa", "postal_code": "1000-001", "street_address": "Av. Roma, 12 - 2 Dto"},{"country_code": "US", "city": "Orlando","street_address":"Fleet Street, 1","postal_code":"32856","country_area":"Florida"}]' http://localhost:8000/addresses/v1/
[{"url":"http://localhost:8000/addresses/v1/83bc78ff-1876-4c96-9fd2-163645012aac/","id":"83bc78ff-1876-4c96-9fd2-163645012aac","country_code":"PT","country_area":"","city":"LISBOA","city_area":"","street_address":"Av. Roma, 12 - 2 Dto","postal_code":"1000-001","sorting_code":"","owner":1},{"url":"http://localhost:8000/addresses/v1/8cd544ef-0dff-4494-89aa-785feae77611/","id":"8cd544ef-0dff-4494-89aa-785feae77611","country_code":"US","country_area":"FL","city":"ORLANDO","city_area":"","street_address":"Fleet Street, 1","postal_code":"32856","sorting_code":"","owner":1}]
```

## Updating dependencies

Update the requirements.in and dev_requirements.in and then run requirements.sh to update the requirements.txt/dev_requirements.txt files.

## Some checks

Run check.sh to run some code checks. Should be used in CI.

## Decisions and assumptions

1. Address model follows the structure needed to validate with the google i18n address validation metadata.
1. Left the default DRF browseable UI to assist discoverability and testing by less experienced developers.
1. Used UUIDs for the address ID to avoid enumeration. ULIDs are a possible alternative that might help with debugging.
1. Added versioning to the addresses endpoints, which might not make sense if the service is just for this API (and then the versioning would be controlled at the API gateway level).

## Future work

1. Add idempotency to the POST requests to simplify client usage.
1. Add support for JWT or equivalent for machine to machine communication.
1. Add support for oAuth2 for frontend/APIs.