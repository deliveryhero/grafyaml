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
from requests import exceptions
from grafana_dashboards.grafana import utils
from typing import List, Dict


class Dashboard(object):
    def __init__(self, base_url: str, session):
        self.url = utils.urljoin(base_url, "api/dashboards/db/")
        self.search_url = utils.urljoin(base_url, "api/search?type=dash-db")
        self.session = session

    def create(self, data: Dict, overwrite: bool = False, folder_id: int = 0) -> None:
        """Create a new dashboard

        :param data: Dashboard model
        :type data: dict
        :param overwrite: Overwrite existing dashboard with newer version or
                          with the same dashboard title
        :type overwrite: bool
        :param folder_id: The id of the folder to save the dashboard in.
        :type folder_id: int

        :raises Exception: if dashboard already exists

        """
        title = str(data.get("title"))
        dashboards = self.find_dashboards_by_title(title, folder_id)

        if len(dashboards) > 1 and overwrite:
            uids = [d.get("uid") for d in dashboards]
            error_msg = (
                f"Found {len(dashboards)} dashboards with name '{title}' in folder {folder_id}. "
                f"Cannot overwrite. UIDs: {uids}"
            )
            raise ValueError(error_msg)

        # If there is already a dashboard with the same name in the same folder, use its UID
        if dashboards and overwrite:
            uid = dashboards[0].get("uid")
            data["uid"] = uid

        dashboard = {
            "dashboard": data,
            "folderId": folder_id,
            "overwrite": overwrite,
        }

        res = self.session.post(self.url, data=json.dumps(dashboard))
        res.raise_for_status()

    def delete(self, name):
        """Delete a dashboard

        :param name: URL friendly title of the dashboard
        :type name: str

        :raises Exception: if dashboard failed to delete

        """
        url = utils.urljoin(self.url, name)
        try:
            res = self.session.delete(url)
            res.raise_for_status()
        except exceptions.HTTPError:
            return None

    def list_dashboards(self) -> Dict:
        """Get a list of all dashboards"""
        response = self.session.get(self.search_url)
        response.raise_for_status()
        return response.json()

    def find_dashboards_by_title(self, title: str, folder_id: int = 0) -> List[Dict]:
        """Find all dashboards with a specific title and optionally in a specific folder

        Args:
            title: The title of the dashboards to find
            folder_id: Optional folder ID to limit the search to

        Returns:
            List of dashboard objects that match the criteria
        """
        dashboards = self.list_dashboards()

        dashboards = list(
            filter(
                lambda x: x.get("title") == title and x.get("folderId") == folder_id,
                dashboards,
            )
        )

        return dashboards
