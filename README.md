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

## Other improvements
1. In addition to Twitter statuses, display other search results
2. Add "search all" endpoint to Django API that will query all sites in parallel

**User story**

As a Kabbage developer, I want to see how you code a lightweight application, so that I can get a feel for a your skills and strengths.

**Acceptance Criteria:**

1. Given a user, when they access your application, then they should be presented with a search box prompting them for a topic - DONE
2. Given a user, when they enter a topic, results from Twitter should be returned - DONE
3. Given a user, when they enter a topic, results from Wikipedia should be returned - DONE
4. Given a user who's performed a search, when they hit the browser's refresh button, results should be refreshed under the same search criteria. - DONE

**Technical notes:**

1. Perform your work in a git repo, and send a tarball of the repo, or post it on GitHub and send us the URL - DONE
2. Use Python, Javascript or some mixture of the two -- play to your strengths :-) - DONE
3. Use the Wikipedia and Twitter APIs - DONE
4. Render the prompt and the results as a Web page - DONE
5. The application must gracefully handle one, the other, or both APIs being down - DONE
6. Include a README that describes the performance profile of your application, highlighting bottlenecks and how you’d tackle them in the future
7. Include unit tests
8. Make sure your submission accurately reflects your development style. - DONE
9. Commit early and often, with good messages. - DONE

**Bonus points:**

* Allow the user to check a box that says “limit result those near me” which restricts the results from Wikipedia and Twitter to a 100 mile radius around the user’s current location
* Deploy to Heroku - DONE
* Impress us :-) - DONE