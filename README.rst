grafyaml
--------

At a glance
+++++++++++

* Free software: Apache license
* Documentation: http://docs.openstack.org/infra/grafyaml/
* Source: http://git.openstack.org/cgit/openstack-infra/grafyaml
* Bugs: https://storyboard.openstack.org/#!/project/818

Overview
++++++++

``grafyaml`` takes descriptions of `Grafana <https://grafana.com/>`__
dashboards in YAML format, and uses them to produce JSON formatted
output suitable for direct import into Grafana.

The tool uses the `Voluptuous
<https://github.com/alecthomas/voluptuous>`__ data validation library
to ensure the input produces a valid dashboard.  Along with
validation, users receive the benefits of YAML markup such as comments
and clearer type support.

For example, here is a minimal dashboard specification

.. code-block:: yaml

  dashboard:
    time:
      from: "2018-02-07T08:42:27.000Z"
      to: "2018-02-07T13:48:32.000Z"
    templating:
      - name: hostname
        type: query
        datasource: graphite
        query: node*
        refresh: true
    title: My great dashboard
    rows:
      - title: CPU Usage
        height: 250px
        panels:
            - title: CPU Usage for $hostname
              type: graph
              datasource: graphite
              targets:
                - target: $hostname.Cpu.cpu_prct_used


``grafyaml`` can be very useful in continuous-integration
environments.  Users can specify their dashboards via a normal review
process and tests can validate their correctness.

A large number of examples are available in the OpenStack
`project-config
<https://git.openstack.org/cgit/openstack-infra/project-config/tree/grafana>`__
repository, which are used to create dashboards on
`<http://grafana.openstack.org>`__.
