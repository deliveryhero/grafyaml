#!/usr/bin/env python3

import yaml
import os
import copy
import logging
from typing import Dict, Any, List, Tuple, Optional

# Cache for loaded row templates across all applications
row_templates_cache: Dict[str, Optional[Dict[str, Any]]] = {}

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def read_configs(
    apps_file: str, base_template_name: str, template_dir: str
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Reads and loads the applications configuration and the base dashboard template.

    Args:
        apps_file: Path to the main applications YAML file (e.g., "apps.yaml").
        base_template_name: Name of the base dashboard template file (e.g., "base_dashboard.yaml").
        template_dir: Directory containing template files (e.g., "templates").

    Returns:
        A tuple containing the parsed applications dictionary and the parsed
        base dashboard template dictionary.

    Raises:
        FileNotFoundError: If required input files are not found.
        yaml.YAMLError: If there's an error parsing the YAML files.
        ValueError: If the loaded YAML does not have the expected top-level structure.
    """
    logging.info(
        f"Reading configuration from '{apps_file}' and base template from '{base_template_name}' in '{template_dir}'"
    )

    # Load applications configuration
    try:
        with open(apps_file, "r") as f:
            parsed_input = yaml.safe_load(f) or {}
        if not isinstance(parsed_input, dict):
            raise ValueError(
                f"Input file '{apps_file}' does not contain a dictionary at the top level. "
                f"Found {type(parsed_input).__name__}."
            )
        logging.info(
            f"Successfully loaded applications config from '{apps_file}'. Found {len(parsed_input)} applications."
        )
    except FileNotFoundError:
        logging.error(f"Applications config file not found: '{apps_file}'")
        raise
    except yaml.YAMLError:
        logging.error(f"Error parsing applications config file: '{apps_file}'")
        raise

    # Load base dashboard template
    base_dashboard_path = os.path.join(template_dir, base_template_name)
    try:
        with open(base_dashboard_path, "r") as f:
            base_dashboard_template = yaml.safe_load(f) or {}
        if not isinstance(base_dashboard_template, dict):
            raise ValueError(
                f"Base dashboard template '{base_dashboard_path}' does not contain a dictionary at the top level. "
                f"Found {type(base_dashboard_template).__name__}."
            )
        logging.info(
            f"Successfully loaded base dashboard template from '{base_dashboard_path}'."
        )
    except FileNotFoundError:
        logging.error(
            f"Base dashboard template file not found: '{base_dashboard_path}'"
        )
        raise
    except yaml.YAMLError:
        logging.error(
            f"Error parsing base dashboard template file: '{base_dashboard_path}'"
        )
        raise

    return parsed_input, base_dashboard_template


def build_app_rows(
    app_name: str,
    row_names: List[str],
    template_dir: str,
) -> List[Dict[str, Any]]:
    """
    Builds the list of row dictionaries for a specific application by loading
    and validating row template files. Caches loaded templates.

    Args:
        app_name: The name of the current application being processed.
        row_names: A list of row template names specified for this application.
        template_dir: Directory containing template files.
        row_templates_cache: A dictionary used to cache loaded row templates.

    Returns:
        A list of valid row dictionaries for the application.
    """
    app_rows_list: List[Dict[str, Any]] = []

    if not isinstance(row_names, list):
        logging.warning(
            f"App '{app_name}' has invalid 'rows' structure. Expected list, "
            f"got {type(row_names).__name__}. No rows will be added from config."
        )
        return []  # Return empty list early

    logging.info(f"Processing {len(row_names)} row(s) for app '{app_name}'...")

    for row_name in row_names:
        if not isinstance(row_name, str) or not row_name:
            logging.warning(
                f"App '{app_name}' has invalid or empty row name '{row_name}'. "
                f"Expected non-empty string. Skipping."
            )
            continue

        # --- Load row template if not already loaded into cache ---
        # Use None as a cache value to signify loading failed previously
        if row_name not in row_templates_cache:
            row_template_path = os.path.join(template_dir, f"{row_name}.yaml")
            try:
                with open(row_template_path, "r") as f:
                    loaded_data = yaml.safe_load(f)
                    # Cache the loaded data (could be None if file was empty)
                    if "rows" in loaded_data and isinstance(loaded_data, dict):
                        row_templates_cache[row_name] = loaded_data["rows"]
                    else:
                        logging.error(
                            f"Row {row_name} is missing top level key rows, skipping"
                        )
                logging.debug(
                    f"Successfully loaded template '{row_name}.yaml' into cache."
                )
            except FileNotFoundError:
                logging.warning(
                    f"Row template file '{row_template_path}' not found for app '{app_name}'. "
                    f"Skipping this row."
                )
                row_templates_cache[row_name] = (
                    None  # Cache None to prevent re-attempting load
                )
            except yaml.YAMLError as e:
                logging.warning(
                    f"Error parsing row template file '{row_template_path}' for app '{app_name}': {e}. "
                    f"Skipping this row."
                )
                row_templates_cache[row_name] = None  # Cache None on error
            except Exception as e:
                logging.warning(
                    f"An unexpected error occurred loading row template '{row_template_path}' for app '{app_name}': {e}. "
                    f"Skipping this row."
                )
                row_templates_cache[row_name] = None  # Cache None on error

        # --- Get the loaded template data from cache ---
        # Check if loading previously failed (cache value is None)
        row_data = row_templates_cache.get(row_name)
        if row_data is None:
            # Warning already printed during loading, just continue
            continue

        # --- Validate the loaded data is a dictionary and looks like a row (has 'panels' list) ---
        # This check assumes a valid single-row template MUST be a dictionary
        # AND contain a 'panels' key which is a list. Adjust validation if needed.
        if isinstance(row_data, dict) and isinstance(row_data.get("panels"), list):
            # Append the single valid row dictionary to the list
            app_rows_list.append(row_data)
            logging.debug(
                f"Appended row from template '{row_name}.yaml' for app '{app_name}'."
            )
        else:
            logging.warning(
                f"Row template '{row_name}.yaml' for app '{app_name}' has invalid structure. "
                f"Expected a dictionary with a 'panels' list at the top level. Skipping."
            )

    return app_rows_list


def process_templating_section(
    dashboard_data: Dict[str, Any], app_config: Dict[str, Any], app_name: str
) -> Dict[str, Any]:
    """
    Processes and merges templating configurations from the base dashboard
    and the application-specific config. Modifies dashboard_data in place.

    Args:
        dashboard_data: The dictionary representing the 'dashboard' key in the base template.
                        Modified in place.
        app_config: The configuration dictionary for the current application.
        app_name: The name of the current application.
    """
    logging.debug(f"Processing templating for app '{app_name}'")

    # Use a dictionary for base templates for faster lookups/updates
    base_templates_list = dashboard_data.get("templating", [])
    if not isinstance(base_templates_list, list):
        logging.warning(
            f"Base dashboard template has invalid 'templating' structure for app '{app_name}'. "
            f"Expected list. Using empty list."
        )
        base_templates_list = []

    base_templates_dict = {
        tmpl.get("name"): tmpl
        for tmpl in base_templates_list
        if isinstance(tmpl, dict) and tmpl.get("name")
    }

    # Add/Update 'app' template (ensuring it exists)
    app_template_config = base_templates_dict.get("app")
    if not isinstance(app_template_config, dict):
        app_template_config = {"name": "app", "type": "constant", "hide": 0}
        base_templates_dict["app"] = app_template_config  # Add/replace in dict

    # Safely update the 'app' template values
    app_template_config["query"] = str(app_name)
    app_template_config.setdefault("current", {})
    app_template_config["current"]["text"] = str(app_name)
    app_template_config["current"]["value"] = str(app_name)
    logging.debug(f"Updated 'app' template for '{app_name}'.")

    # Add or override base templates with app-specific templates
    app_templates_list = app_config.get("templating", [])
    if not isinstance(app_templates_list, list):
        logging.warning(
            f"App '{app_name}' has invalid 'templating' structure. Expected list, "
            f"got {type(app_templates_list).__name__}. No app-specific templates will be added."
        )
        app_templates_list = []  # Use empty list

    for template in app_templates_list:
        if isinstance(template, dict) and template.get("name"):
            base_templates_dict[template["name"]] = (
                template  # Add or overwrite using name as key
            )
            logging.debug(
                f"Added/Overrode template '{template.get('name')}' for '{app_name}'."
            )
        else:
            logging.warning(
                f"App '{app_name}' contains an invalid template definition: {template}. "
                f"Expected a dictionary with a 'name' key. Skipping."
            )

    # Convert the templates dictionary back to a list for the final dashboard structure
    dashboard_data["templating"] = list(base_templates_dict.values())
    logging.debug(f"Finished processing templating for app '{app_name}'.")

    return dashboard_data


def write_dashboard_file(
    app_name: str, output_dir: str, dashboard_data: Dict[str, Any]
) -> None:
    """
    Writes the generated dashboard dictionary to a YAML file.

    Args:
        app_name: The name of the application.
        output_dir: The output directory.
        dashboard_data: The dictionary representing the dashboard structure.
    """
    output_file_path = os.path.join(output_dir, f"{app_name}.yaml")
    logging.info(f"Writing dashboard to '{output_file_path}'")
    try:
        with open(output_file_path, "w") as f:
            # Use default_flow_style=False for a more human-readable output
            yaml.dump(dashboard_data, f, default_flow_style=False)
        logging.info(f"Successfully generated '{output_file_path}'")
    except (IOError, yaml.YAMLError) as e:
        logging.error(f"Error writing output file '{output_file_path}': {e}")
    except Exception as e:
        logging.error(
            f"An unexpected error occurred while writing output file '{output_file_path}': {e}"
        )


def main():
    """
    Main function to generate Grafana dashboards.
    """
    # --- Configuration ---
    apps_filename = "apps.yaml"
    template_dir = "templates"
    output_dir = "rendered_dashboards"
    base_dashboard_template_name = "base_dashboard.yaml"

    logging.info("Starting dashboard generation process.")

    # --- Safety: Create output directory if it doesn't exist ---
    try:
        os.makedirs(output_dir, exist_ok=True)
        logging.info(f"Ensured output directory '{output_dir}' exists.")
    except OSError as e:
        logging.error(f"Failed to create output directory '{output_dir}': {e}")
        return  # Cannot proceed if output directory cannot be created

    # --- Speed & Safety: Load base configuration and templates once ---
    try:
        apps_config, base_dashboard_raw = read_configs(
            apps_filename, base_dashboard_template_name, template_dir
        )
    except (FileNotFoundError, yaml.YAMLError, ValueError) as e:
        logging.error(f"Failed to load initial configuration files. Exiting. {e}")
        return  # Critical error, cannot proceed

    # --- Process each application ---
    if not apps_config:
        logging.warning(
            "No applications found in the input configuration. Nothing to generate."
        )

    for app_name, app_config in apps_config.items():
        # Ensure app_config is a dictionary and app_name is usable
        if not isinstance(app_name, str) or not isinstance(app_config, dict):
            logging.warning(
                f"Skipping invalid configuration entry. Expected key (app name) to be string "
                f"and value to be dictionary. Got {type(app_name).__name__}: {app_name} "
                f"- {type(app_config).__name__}."
            )
            continue

        logging.info(f"Processing application '{app_name}'")

        # --- Accuracy & Speed: Deep copy the base template for each app ---
        # We need a deep copy so modifications for one app don't affect others
        dashboard_full_structure = copy.deepcopy(base_dashboard_raw)

        # Access the main dashboard data dictionary safely
        dashboard_data = dashboard_full_structure.get("dashboard")
        if not isinstance(dashboard_data, dict):
            logging.warning(
                f"Base dashboard template structure invalid for app '{app_name}'. "
                f"Missing or invalid 'dashboard' key. Skipping generation for this app."
            )
            continue

        # --- Accuracy: Set correct name for dashboard ---
        dashboard_data["title"] = str(app_name)
        logging.debug(f"Set dashboard title to '{app_name}'.")

        # --- Process Templating ---
        dashboard_data = process_templating_section(
            dashboard_data, app_config, app_name
        )

        # --- Build and Assign Rows ---
        rows_config = app_config.get("rows", [])  # Get rows list safely from app config

        dashboard_data["panels"] = build_app_rows(
            app_name,
            rows_config,
            template_dir,
        )

        # --- Override Tags if specified ---
        app_tags = app_config.get("tags")
        if app_tags is not None:  # Allows setting tags to None/empty list in input
            if (
                isinstance(app_tags, list) or app_tags is None
            ):  # Ensure it's a list or None
                dashboard_data["tags"] = app_tags
                logging.debug(f"Overrode tags for '{app_name}': {app_tags}")
            else:
                logging.warning(
                    f"App '{app_name}' has invalid 'tags' structure: {app_tags}. "
                    f"Expected list or null. Skipping tag override."
                )

        if "permissions" in app_config:
            dashboard_full_structure["permissions"] = app_config.get("permissions", [])

        # --- Write Output File ---
        # Pass the dictionary that represents the content *under* the top-level 'dashboard' key
        write_dashboard_file(
            app_name=app_name, output_dir=output_dir, dashboard_data=dashboard_full_structure
        )

    logging.info("Dashboard generation process completed.")


if __name__ == "__main__":
    main()
