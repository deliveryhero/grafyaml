from urllib.parse import urlunsplit
import requests
import configparser
import logging
import json

from dogpile.cache.region import make_region
from typing import Dict, Optional, List, Dict, Any, Tuple


LOG = logging.getLogger(__name__)

cache = make_region(name="team_user_cache").configure(
    "dogpile.cache.memory", expiration_time=3600
)


class Permissions:
    def __init__(self, url: str, session: requests.Session):
        self.session: requests.Session = session
        self.config: configparser.ConfigParser = configparser.ConfigParser()
        self.permission_levels: Dict[str, int] = {"view": 1, "edit": 2, "admin": 4}
        self.base_url: str = url
        self.overwrite: bool = False

    def get_dashboard_permissions(self, uid: str) -> Optional[List[Dict[str, Any]]]:
        """Fetches the current permissions for a given dashboard UID."""
        url = f"{self.base_url}/api/dashboards/uid/{uid}/permissions"
        LOG.debug(f"Fetching current permissions for dashboard UID: {uid}")
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def _reconcile_permissions(
        self, dashboard_uid: str, permissions_strings: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Reconciles current dashboard permissions with a list of desired permissions.
        It updates existing permissions or adds new ones, preserving others.
        """
        current_permissions = self.get_dashboard_permissions(dashboard_uid)

        if current_permissions is None:
            current_permissions = []

        reconciled_permissions_map: Dict[Any, Dict[str, Any]] = {}

        # Add all existing permissions to the map first
        if not self.overwrite:
            for perm in current_permissions:
                for subject_key in ["teamId", "userId", "role"]:
                    if subject_key:
                        subject_id = perm.get(subject_key)
                        if subject_id not in [0, ""]:
                            reconciled_permissions_map[(subject_key, subject_id)] = perm
                    else:
                        logging.warning(
                            f"Unknown subject type found in existing permission for dashboard {dashboard_uid}: {perm}"
                        )
                        reconciled_permissions_map[
                            ("unknown", hash(json.dumps(perm)))
                        ] = perm

        for permission_str in permissions_strings:

            subject, identifier, perm = self._parse_permission_string(permission_str)

            subject_key, subject_id = self._get_subject_id(subject, identifier)

            if subject_id is None:
                raise Exception(
                    f"Could not resolve subject '{identifier}' of type '{subject}'"
                )

            permission_level = self.permission_levels.get(perm.lower())
            if permission_level is None:
                raise Exception(
                    f"Invalid permission role '{perm}' specified. Valid roles are: {', '.join(self.permission_levels.keys())}"
                )

            permission_item = {
                subject_key: subject_id,
                "permission": permission_level,
            }

            subject_map_key = (subject_key, subject_id)

            # Check if this subject already has a permission in the map
            if subject_map_key in reconciled_permissions_map:
                existing_perm = reconciled_permissions_map[subject_map_key]
                if existing_perm.get("permission") != permission_level:
                    LOG.debug(
                        f"Updating existing permission for {subject} '{identifier}' on dashboard {dashboard_uid} "
                        f"from {existing_perm.get('permission')} to {permission_level}."
                    )
                    reconciled_permissions_map[subject_map_key] = permission_item
                else:
                    LOG.debug(
                        f"{subject} '{identifier}' already has permission {permission_level} on dashboard {dashboard_uid}. No change needed."
                    )
            else:
                LOG.debug(
                    f"Adding new permission for {subject} '{identifier}' (level {permission_level}) to dashboard {dashboard_uid}."
                )
                reconciled_permissions_map[subject_map_key] = permission_item

        return list(reconciled_permissions_map.values())

    def _update_dashboard_permissions(
        self, uid: str, permissions: List[Dict[str, Any]]
    ):
        """
        Sends the complete list of reconciled permissions to the Grafana API to update a dashboard.
        """
        url = f"{self.base_url}/api/dashboards/uid/{uid}/permissions"
        payload = {"items": permissions}

        LOG.debug(
            f"Attempting to set permissions for dashboard UID {uid} with payload: {json.dumps(payload, indent=2)}"
        )

        response = self.session.post(url, json=payload)
        response.raise_for_status()
        LOG.debug(f"Successfully updated permissions for dashboard UID: {uid}")
        return response.json()

    def update(
        self,
        dashboard_uid: str,
        permissions: Dict[str, Any],
    ):
        """
        Main method to update permissions for a single dashboard based on a list of desired permission strings.
        """

        strategy = permissions.get("strategy", "")
        permissions_strings = permissions.get("grants", [])

        LOG.debug(
            f"Updating permissions for dashboard {dashboard_uid}: {json.dumps(permissions_strings, indent=2)}"
        )

        if strategy == "merge":
            self.overwrite = False
        elif strategy == "replace":
            self.overwrite = True
        else:
            raise Exception(
                f"Invalid permissions strategy '{strategy}'. Valid strategies are 'merge' and 'replace'."
            )

        self._get_teams()

        reconciled_permissions = self._reconcile_permissions(
            dashboard_uid=dashboard_uid, permissions_strings=permissions_strings
        )

        if not reconciled_permissions:
            LOG.warning(
                f"No valid permissions to apply for dashboard '{dashboard_uid}'. Check logs for parsing or subject resolution errors."
            )
            return

        resp = self._update_dashboard_permissions(
            uid=dashboard_uid, permissions=reconciled_permissions
        )
        return resp.get("items")

    @cache.cache_on_arguments()
    def _get_team_id(self, name: str) -> Optional[int]:
        """Fetches the ID of a Grafana team by its name."""
        url = f"{self.base_url}/api/teams/search?name={name}"
        logging.debug(f"Searching for team: {name}")

        response = self.session.get(url)
        response.raise_for_status()
        teams = response.json().get("teams")
        if teams and len(teams) > 0:
            return teams[0].get("id")
        logging.warning(f"Team '{name}' not found.")
        return None

    @cache.cache_on_arguments()
    def _get_user_id(self, email_or_login: str) -> Optional[int]:
        """Fetches the ID of a Grafana user by their email or login."""
        url = f"{self.base_url}/api/org/users/lookup?loginOrEmail={email_or_login}"
        logging.debug(f"Searching for user: {email_or_login}")  # Changed to debug

        response = self.session.get(url)
        response.raise_for_status()
        users = response.json()
        if users:
            return users[0].get("userId")
        logging.warning(f"User '{email_or_login}' not found.")
        return None

    def _get_teams(self):
        """Get all teams"""
        url = f"{self.base_url}/api/teams/search"
        logging.debug("Searching for teams")

        response = self.session.get(url)
        response.raise_for_status()
        teams = response.json().get("teams", [])

        if "teams" not in self.config.sections():
            self.config.add_section("teams")

        for team in teams:
            team_name = team.get("name")
            team_key = team_name.replace(" ", "_").lower()
            self.config.set("teams", team_key, team_name)

    def _get_subject_id(
        self, subject: str, subject_identifier: str
    ) -> Tuple[str, Optional[Any]]:
        """Resolves the subject type and ID based on the provided type and name/ID."""
        if subject.lower() == "team":
            actual_grafana_name = self.config.get(
                section="teams",
                option=subject_identifier.lower(),
                fallback=subject_identifier,
            )
            subject_id = self._get_team_id(actual_grafana_name)
            return "teamId", subject_id
        elif subject.lower() == "user":
            subject_id = self._get_user_id(subject_identifier)
            return "userId", subject_id
        elif subject.lower() == "role":
            return "role", subject_identifier
        else:
            raise ValueError(
                f"Unknown subject type '{subject}'. Supported types are 'team','user' and role."
            )

    def _parse_permission_string(self, permission_string: str) -> Tuple[str, str, str]:
        """
        Parses a string like "subject:identifier:permission"
        into three separate strings (subject,identifier, permission).
        Raises ValueError if the format is incorrect.
        """
        parts = permission_string.split(":")
        if len(parts) == 3:
            return parts[0], parts[1], parts[2]
        else:
            raise ValueError(
                f"Permission string must be in format 'type:identifier:level'. Got: '{permission_string}'"
            )
