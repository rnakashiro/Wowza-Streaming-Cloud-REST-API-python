# Wowza-Streaming-Cloud-REST-API-python


A lightweight API client of Wowza Streaming Cloud REST API for Python 2.x.  

This is written for a project use, so there aren't all features for the API Spec.  
But you can easily extend this script to your project, if you love python :wink:


## Usage

```python
api_key    = 'xxxxxx'
access_key = 'xxxxxx'

api_client = WawzaAPIClient(api_key=api_key, access_key=access_key)
res = api_client.fetch_live_streams()
```
