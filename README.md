# github-scraper-spark-delta

## Rate Limits

GitHub API rate limits apply to this scraper. The limits are as follows:

* Unauthenticated: 60 requests/hour
* Authenticated: 5,000 requests/hour (add a [personal access token](https://github.com/settings/tokens) to headers)

## Available Endpoints

### User Data

Retrieve user data with the following endpoint:

* `GET /users/{username}`
* Example: `https://api.github.com/users/onnx`

### Repository Data

Retrieve repository data with the following endpoint:

* `GET /repos/{owner}/{repo}`
* Example: `https://api.github.com/repos/onnx/onnx`

### Search

Search for repositories with the following endpoint:

* `GET /search/repositories?q={query}`
* Example: `https://api.github.com/search/repositories?q=stars:>1000`

### Repository Issues

Retrieve repository issues with the following endpoint:

* `GET /repos/{owner}/{repo}/issues`
* Example: `https://api.github.com/repos/facebook/react/issues`
