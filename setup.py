from setuptools import setup

setup(
    name="grafyaml",
    version="1.3.0",
    url="https://github.com/deliveryhero/grafyaml",
    license="Apache v2.0",
    description="A nice and easy way to template Grafana dashboards in YAML",
    long_description=open("README.md", encoding="utf-8").read(),
    packages=[
        "grafana_dashboards",
        "grafana_dashboards/grafana",
        "grafana_dashboards/schema",
        "grafana_dashboards/schema/panel",
        "grafana_dashboards/schema/template",
    ],
    entry_points={
        "console_scripts": ["grafana-dashboard=grafana_dashboards.cmd:main"],
    },
    install_requires=[
        "dogpile.cache",
        "python-slugify",
        "PyYAML>=3.1.0",
        "requests",
        "six>=1.6.0",
        "voluptuous<=0.10.5",
    ],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
)
