# -*- coding:utf-8 -*-
# written in Jul 2018

# doc: https://sandbox.cloud.wowza.com/api/v1/docs#operation/createLiveStream

import json
import requests


class WowzaAPIException(Exception):

    def __init__(self, message, code):
        super(WowzaAPIException, self).__init__(message)
        self.code = code


class WowzaAPIClient:

    base_url = 'https://api.cloud.wowza.com/api/v1'

    def __init__(self, api_key='', access_key=''):
        self.api_key = api_key
        self.access_key = access_key


    ### common utilities
    @property
    def auth_headers(self):
        return {
            'wsc-api-key': self.api_key, 
            'wsc-access-key': self.access_key, 
            'content-type': 'application/json'
        }

    def validate_json(self, response):
        try:
            if response.status_code == 204:
                return {}
            json_data = response.json()
            if 'meta' in json_data:
                meta = json_data['meta']
                if 'message' in meta and 'status' in meta:
                    raise WowzaAPIException(meta['message'], meta['status'])
            return json_data
        except Exception as e:
            raise e


    ### each methods
    def get_json(self, endpoint, params={}):
        api_url = self.base_url + endpoint
        response = requests.get(api_url, params=params, headers=self.auth_headers)
        return self.validate_json(response)

    def post_json(self, endpoint, params={}):
        api_url = self.base_url + endpoint
        response = requests.post(api_url, data=json.dumps(params), headers=self.auth_headers)
        return self.validate_json(response)

    def put_json(self, endpoint, params={}):
        api_url = self.base_url + endpoint
        response = requests.put(api_url, data=json.dumps(params), headers=self.auth_headers)
        return self.validate_json(response)

    def patch_json(self, endpoint, params={}):
        api_url = self.base_url + endpoint
        response = requests.patch(api_url, data=json.dumps(params), headers=self.auth_headers)
        return self.validate_json(response)

    def delete_json(self, endpoint, params={}):
        api_url = self.base_url + endpoint
        response = requests.delete(api_url, data=json.dumps(params), headers=self.auth_headers)
        return self.validate_json(response)


    ### LIVE STREAMS endpoints
    '''
    create live-stream params
     - req aspect_ratio_height: int
     - req aspect_ratio_width: int
     - req billing_mode: pay_as_you_go, twentyfour_seven
     - req broadcast_location: asia_pacific_australia, asia_pacific_india, asia_pacific_japan, ...
     - req encoder: wowza_streaming_engine, wowza_gocoder, ipcamera, other_rtmp, other_rtsp, ...
     - req name: str
     - req transcoder_type: transcoded, passthrough
     - opt closed_caption_type: none, cea, on_text, both
     - opt delivery_method: pull, cdn, push
     - opt delivery_protocols: rtmp, rtsp, wowz
     - opt delivery_type: single-bitrate, multi-bitrate
     - opt disable_authentication: false, true
     - opt hosted_page: true, false
     - opt hosted_page_description: str
     - opt hosted_page_logo_image: str-Base64-encoded
     - opt hosted_page_sharing_icons: true, false
     - opt hosted_page_title: str
     - opt low_latency: false, true
     - opt password: str
     - opt player_countdown: false, true
     - opt player_countdown_at: str-datetime (YYYY-MM-DD HH:MM:SS)
     - opt player_logo_image: str-Base64-encoded
     - opt player_logo_position: top-left, top-right, bottom-left, bottom-right
     - opt player_responsive: true, false
     - opt player_type: original_html5, wowza_player
     - opt player_video_poster_image: str-Base64-encoded
     - opt player_width: int (640)
     - opt recording: false, true
     - opt remove_hosted_page_logo_image: false, true
     - opt remove_player_logo_image: false, true
     - opt remove_player_video_poster_image: false, true
     - opt source_url: str
     - opt target_delivery_protocol: hls-https, hls-hds
     - opt use_stream_source: false, true
     - opt username: str
     - opt video_fallback: false, true
    '''
    def create_live_stream(self, live_stream_params={}):
        return self.post_json('/live_streams', params={ 'live_stream': live_stream_params })

    def fetch_live_streams(self, page=0, per_page=10):
        return self.get_json('/live_streams', params={ 'page': page, 'per_page': per_page })

    def fetch_live_stream(self, live_stream_id):
        return self.get_json('/live_streams/%s' % (live_stream_id))

    # required: aspect_ratio_height, aspect_ratio_width, encoder, name
    def update_live_stream(self, live_stream_id, live_stream_params={}):
        return self.patch_json('/live_streams/%s' % (live_stream_id), params={ 'live_stream': live_stream_params })

    def delete_live_stream(self, live_stream_id):
        return self.delete_json('/live_streams/%s' % (live_stream_id))

    def start_live_stream(self, live_stream_id):
        return self.put_json('/live_streams/%s/start' % (live_stream_id))

    def stop_live_stream(self, live_stream_id):
        return self.put_json('/live_streams/%s/stop' % (live_stream_id))

    def reset_live_stream(self, live_stream_id):
        return self.put_json('/live_streams/%s/reset' % (live_stream_id))

    def regenerate_connection_code_live_stream(self, live_stream_id):
        return self.put_json('/live_streams/%s/regenerate_connection_code' % (live_stream_id))

    def fetch_live_stream_thumbnail(self, live_stream_id):
        return self.get_json('/live_streams/%s/thumbnail_url' % (live_stream_id))

    def fetch_live_stream_state(self, live_stream_id):
        return self.get_json('/live_streams/%s/state' % (live_stream_id))

    def fetch_live_stream_stats(self, live_stream_id):
        return self.get_json('/live_streams/%s/stats' % (live_stream_id))


