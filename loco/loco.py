#!/usr/bin/env python3
import sys
import os

import click
#from google_location_client import client as gmapsclient
#from here_location_client import client as hmapclient
from loco.loco_fastapi import service as httpsrv
import loco.controller as controller

@click.group()
def cli():
    pass

@click.command()
def proxy():
    print ("in proxy")
    httpsrv.start()
    return True

@click.command()
@click.argument('address')
def query(address):
    controller.search(address)
    return True

def main():
    cli()
    return True

cli.add_command(query)
cli.add_command(proxy)

if __name__ == "__main__":
    sys.exit(main())