import click
import logging
import pathlib

import mirror

__version__ = "0.0.1-pre1"

@click.version_option(prog_name="mirror", version=__version__)
@click.group()
def main():
    """
    Mirror is a tool for mirroring files and directories to a remote server.
    """
    pass

@main.command("crontab")
@click.option("-u", "--user", default="root", help="User to run the cron job as.")
@click.option("-c", "--config", default="config.json", help="Path to the config file.")
def crontab(user, config):
    """
    Generate a crontab file from the config file.
    """
    config = mirror.config.load(config)
    crontab = mirror.crontab.generate(config, user)
    print(crontab)