# Copyright (c) 2012 Qumulo, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import time

import qumulo.lib.request as request
import qumulo.lib.util as util

@request.request
def login(conninfo, credentials, username, password):
    method = "POST"
    uri = "/v1/login"

    login_info = {
        'username': util.parse_ascii(username, 'username'),
        'password': util.parse_ascii(password, 'password'),
    }
    resp = request.rest_request(conninfo, credentials, method, uri,
                                body=login_info)
    # Authorization uses deltas in time, so we store this systems unix epoch as
    # the issue date.  That way time deltas can be computed locally.
    # Server uses its own time deltas so the clocks must tick at the same rate.
    resp[0]['issue'] = int(time.time())
    return resp

@request.request
def change_password(conninfo, credentials, old_password, new_password):
    "Unlike SetUserPassword, acts implicitly on logged in user"

    method = "POST"
    uri = "/v1/setpassword"
    body = {
        'old_password': util.parse_ascii(old_password, 'old password'),
        'new_password': util.parse_ascii(new_password, 'new password')
    }

    return request.rest_request(conninfo, credentials, method, uri, body=body)

@request.request
def who_am_i(conninfo, credentials):
    "Same as GET on user/<current_id>"
    return request.rest_request(conninfo, credentials, "GET", "/v1/who-am-i")
