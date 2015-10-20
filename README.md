# multi-search
Search aggregator for multiple sites

## Viewing the application
You can view the application at [https://multisearch-client-jdeveloperw.c9.io](https://multisearch-client-jdeveloperw.c9.io)

## Architecture
The multisearch application is divided into two separate services:

1. nodejs server which serves the static HTML, Javascript (AngularJS), and CSS used by the client (see client/)
2. Django server which provides the API endpoints used by the client (see server/)

## Performance improvements
1. Perform asynchronous loads of resources in the client
2. Cache results from Twitter and return them when the Twitter API is throttling requests
3. Have a persistent Twitter client that only refreshes when authentication expires.

## Other improvements
1. In addition to Twitter statuses, display other search results
2. Add "search all" endpoint to Django API that will query all sites in parallel
3. Add client tests