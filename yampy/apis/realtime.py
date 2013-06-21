# Copyright (c) Microsoft Corporation
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# THIS CODE IS PROVIDED *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY
# IMPLIED WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR
# PURPOSE, MERCHANTABLITY OR NON-INFRINGEMENT.
#
# See the Apache Version 2.0 License for specific language governing
# permissions and limitations under the License.

import json
import requests

class RealtimeAPI(object):
    """
    Provides an interface for accessing the realtime related endpoints of the
    Yammer API. You should not instantiate this class directly; use the
    :meth:`yampy.Yammer.realtime` method instead.
    """
    def __init__(self, client):
        """
        Initializes a new MessagesAPI that will use the given ``client`` object
        to make HTTP requests.
        """
        self._client = client

        self.version = "1.0"
        self.minimumVersion = "0.9"
        #self.channel = "/meta/handshake"
        self.supportedConnectionTypes = ["long-polling"]
        self.current_id = 1

    def handshake(self, messages, **kwargs):
        self.base_url = messages.meta.realtime.uri
        self.authentication_token = messages.meta.realtime.authentication_token
        self.channel_id = messages.meta.realtime.channel_id

        payload = [{
            "ext" : { "token" : self.authentication_token},
            "version" : self.version,
            "minimumVersion" : self.minimumVersion,
            "channel" : "/meta/handshake",
            "supportedConnectionTypes" : self.supportedConnectionTypes,
            "id" : self._get_id()
        }]
        print(payload)

        ret = requests.post(
            url=self._build_url("/handshake"),
            headers=self._build_headers(),
            data=json.dumps(payload),
            params=kwargs
        )
        response = self._client._parse_response(ret)[0]
        print response
        #self.advice = response.advice
        self.client_id = response.clientId

        return response

    def subscribe(self, **kwargs):
  
        payload = [{
            "channel" : "/meta/subscribe",
            "subscription" : "/feeds/%s/primary" % self.channel_id,
            "id" : self._get_id(),
            "clientId" : self.client_id
        },{
            "channel" : "/meta/subscribe",
            "subscription" : "/feeds/%s/secondary" % self.channel_id,
            "id" : self._get_id(),
            "clientId" : self.client_id
        }]
        print(payload)
        ret = requests.post(
            url=self._build_url("/"),
            headers=self._build_headers(),
            data=json.dumps(payload),
            params=kwargs
        )
        response = self._client._parse_response(ret)
        return response

    def connect(self, **kwargs):
        payload = [{
            "channel" : "/meta/connect",
            "connectionType": "long-polling",
            "id" : self._get_id(),
            "clientId" : self.client_id
        }]
        print(payload)
        response = requests.post(
            url=self._build_url("/"),
            headers=self._build_headers(),
            data=json.dumps(payload),
            params=kwargs
        )
        return self._client._parse_response(response)

    def _build_url(self, path):
        return self.base_url + path

    def _build_headers(self):   
        return {
            "content-type" : "application/json"
        }

    def _get_id(self):
        _id = self.current_id
        self.current_id += 1
        return _id

