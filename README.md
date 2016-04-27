# Testing Django Applications

April 28, 2016
Boston, MA

## Setup

* Install homebrew
* `brew install chromedriver`
* `npm install`
* Set up [facebook application](https://developers.facebook.com/apps/)
* Create `meetup/meetup/secrets.py` and `meetup/meetup/secrets_test.py` with `FB_APP_ID` and `FB_APP_SECRET`

## Running

* `make serve`
* `open http://localhost:8000`

## Testing

* `make test`
