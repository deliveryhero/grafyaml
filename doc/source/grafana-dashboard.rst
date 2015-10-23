=================
grafana-dashboard
=================

SYNOPSIS
========

``grafana-dashboard`` [options] <command> [<args>...]

DESCRIPTION
===========

``grafana-dashboard`` is a CLI command to update Grafana dashboards from yaml
files.

OPTIONS
=======

-h, --help            Show this help message and exit
--config-file CONFIG  Path to a config file to use. The default files used
                      is: /etc/grafyaml/grafyaml.conf
--debug               Print debugging output (set logging level to DEBUG
                      instead of default INFO level)
--version             Show program's version number and exit

COMMANDS
========

Delete Command
--------------

``grafana-dashboard`` [options] delete <path>

Delete each specified dashboard from the parsed yaml files.

Update Command
--------------

``grafana-dashboard`` [options] update <path>

Updates each specified dashboard to the lastest layout from parsed yaml files.

FILES
=====

/etc/grafyaml/grafyaml.conf

AUTHOR
======

.. include:: ../../AUTHORS
