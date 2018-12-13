from setuptools import setup

setup(name = "py-opensmtpd-eventlog",
      version = "0.0.1",
      description = "py-opensmtpd-eventlog is a logger for OpenSMTPD events",
      author = "Gilles Chehade",
      author_email = "gilles@poolp.org",
      packages = [ "opensmtpd_eventlog" ],
      scripts = [
          "scripts/filter-eventlog",
      ],
)
