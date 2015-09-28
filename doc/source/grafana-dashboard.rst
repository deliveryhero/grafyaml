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

-h, --help          Show the help.
--config-dir DIR    Path to a config directory to pull \*.conf files from. This
                    file set is sorted, so as to provide a predictable parse
                    order if individual options are over-ridden. The set is
                    parsed after the file(s) specified via previous
                    --config-file, arguments hence over-ridden options in the
                    directory take precedence.
--config-file PATH  Path to a config file to use. Multiple config files can be
                    specified, with values in later files taking precedence. The
                    default files used are: None.
-d, --debug         Print debugging output(set logging level to DEBUG
                    instead of default WARNING level).
-v, --verbose       Print more verbose output (set logging level to INFO
                    instead of default WARNING level).
--version           Show program's version number and exit.

COMMANDS
========

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
