# Copyright 2015 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json
import requests_mock
from testtools import TestCase

from grafana_dashboards.grafana import Grafana

CREATE_NEW_DASHBOARD = {
    "meta": {
        "canSave": True,
        "created": "0001-01-01T00:00:00Z",
        "canStar": True,
        "expires": "0001-01-01T00:00:00Z",
        "slug": "new-dashboard",
        "type": "db",
        "canEdit": True,
    },
    "dashboard": {"rows": [], "id": 1, "version": 0, "title": "New dashboard"},
}

DASHBOARD_NOT_FOUND = {"message": "Dashboard not found"}


class TestCaseGrafana(TestCase):
    def setUp(self):
        super(TestCaseGrafana, self).setUp()
        self.url = "http://localhost"
        self.grafana = Grafana(self.url)

    def test_init(self):
        grafana = Grafana(self.url)
        self.assertNotIn("Authorization", grafana.dashboard.session.headers)

    def test_init_apikey(self):
        apikey = "eyJrIjoiT0tTcG1pUlY2RnVKZTFVaDFsNFZXdE9ZWmNrMkZYbk"
        grafana = Grafana(self.url, apikey)
        headers = grafana.dashboard.session.headers
        self.assertIn("Authorization", headers)
        self.assertEqual(headers["Authorization"], "Bearer %s" % apikey)

    @requests_mock.Mocker()
    def test_create_dashboard_new(self, mock_requests):
        # Mock the search endpoint
        mock_requests.get(
            "http://localhost/api/search?type=dash-db",
            status_code=200,
            json=[],  # No existing dashboards
        )

        # Mock the create dashboard endpoint
        mock_requests.post(
            "http://localhost/api/dashboards/db/",
            status_code=200,
            json={"message": "Dashboard created"},
        )

        data = {
            "dashboard": {
                "title": "Test Dashboard",
                "rows": [],
                "id": None,
                "version": 0,
                "uid": None,
            },
            "slug": "test-dashboard",
        }

        self.grafana.dashboard.create(data=data["dashboard"])
        self.assertEqual(mock_requests.call_count, 2)

        # Verify the request body
        last_request = mock_requests.last_request
        request_data = json.loads(last_request.body)
        self.assertEqual(request_data["dashboard"], data["dashboard"])
        self.assertFalse(request_data["overwrite"])
        self.assertEqual(request_data["folderId"], 0)

    @requests_mock.Mocker()
    def test_create_dashboard_overwrite(self, mock_requests):
        # Mock existing dashboard
        mock_requests.get(
            "http://localhost/api/search?type=dash-db",
            status_code=200,
            json=[
                {
                    "title": "Test Dashboard",
                    "uid": "existing-uid",
                    "folderId": 0,
                    "id": 1,
                }
            ],
        )

        # Mock the create dashboard endpoint
        mock_requests.post(
            "http://localhost/api/dashboards/db/",
            status_code=200,
            json={
                "title": "Test Dashboard",
                "uid": "existing-uid",
                "folderId": 0,
                "id": 1,
            },
        )

        data = {
            "dashboard": {
                "title": "Test Dashboard",
                "rows": [],
                "id": 1,
                "version": 0,
                "uid": "existing-uid",
            },
            "slug": "test-dashboard",
        }

        uid = self.grafana.dashboard.create(data=data["dashboard"], overwrite=True)
        self.assertEqual(mock_requests.call_count, 2)
        self.assertEqual(uid, "existing-uid")

    @requests_mock.Mocker()
    def test_update_permissions(self, mock_requests):
        mock_requests.get(
            "http://localhost/api/teams/search",
            status_code=200,
            json={
                "teams": [
                    {
                        "id": 1,
                        "name": "Team 1",
                    }
                ]
            },
        )

        mock_requests.get(
            "http://localhost/api/dashboards/uid/existing-uid/permissions",
            status_code=200,
            json=[],
        )

        mock_requests.post(
            "http://localhost/api/dashboards/uid/existing-uid/permissions",
            status_code=200,
            json={
                "items": [
                    {"teamId": 1, "permission": 4},
                    {"teamId": 2, "permission": 2},
                ]
            },
        )

        permissions = ["team:admins:admin", "team:developers:edit"]

        items = self.grafana.permissions.update(
            dashboard_uid="existing-uid",
            permissions_strings=permissions,
            permissions_strategy="merge",
        )

        self.assertEqual(mock_requests.call_count, 5)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["teamId"], 1)
        self.assertEqual(items[0]["permission"], 4)
        self.assertEqual(items[1]["teamId"], 2)
        self.assertEqual(items[1]["permission"], 2)

    @requests_mock.Mocker()
    def test_delete_dashboard(self, mock_requests):
        mock_requests.delete("/api/dashboards/db/new-dashboard", status_code=200)
        self.grafana.dashboard.delete("new-dashboard")
