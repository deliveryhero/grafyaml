#!/usr/bin/env python3

import yaml
import os


def find_template_index(template, template_list):
    index = 0
    for item in template_list:
        if item["name"] == template["name"]:
            return index
        else:
            index = index + 1
    index = -1
    return index


def main():
    filename = "apps.yaml"
    template_dir_name = "templates"

    dashboard_list = open(filename)
    parsed_input = yaml.load(dashboard_list, Loader=yaml.FullLoader)

    # Generate dashboard for each application
    for appname in parsed_input.keys():
        base_dashboard_filename = template_dir_name + "/base_dashboard.yaml"
        base_dashboard_file = open(base_dashboard_filename)
        dashboard = yaml.load(base_dashboard_file, Loader=yaml.FullLoader)

        # Set correct name for dashboard
        dashboard["dashboard"]["title"] = appname
        # Add app name as constant template
        for app_template in dashboard["dashboard"]["templating"]:
            if app_template["name"] == "app":
                app_template["query"] = appname
                app_template["current"]["text"] = appname
                app_template["current"]["value"] = appname
                break

        # Add rows from app_dashboards to generated dashboard
        rows = []
        for row in parsed_input[appname]["rows"]:
            template_file_name = template_dir_name + "/" + row + ".yaml"
            row_template = open(template_file_name)
            parsed_row = yaml.load(row_template, Loader=yaml.FullLoader)["rows"]
            rows.append(parsed_row)

        # Add or override the default templates with the templates
        # specified in the app dashboards file
        if "templating" in parsed_input[appname]:
            for template in parsed_input[appname]["templating"]:
                index = find_template_index(
                    template, dashboard["dashboard"]["templating"]
                )
                if index == -1:
                    dashboard["dashboard"]["templating"].append(template)
                else:
                    dashboard["dashboard"]["templating"][index] = template

        # Override tags if specified
        if "tags" in parsed_input[appname]:
            dashboard["dashboard"]["tags"] = parsed_input[appname]["tags"]

        dashboard["dashboard"]["rows"] = rows

        output_file_name = "rendered_dashboards/" + "/" + appname + ".yaml"
        output_file = open(output_file_name, "w")
        output_file.write(yaml.dump(dashboard))


if __name__ == "__main__":
    main()
