#!/usr/bin/env python3
import sys
import os

import click
from loguru import logger

from loco.loco_fastapi import service as httpsrv
import loco.controller as controller

@click.group()

@click.option('--google_api_key')
@click.option('--here_app_id')
@click.option('--here_app_code')
def cli(google_api_key,here_app_id,here_app_code):
    '''
    This applciation will return the lat/lon from any one of several
    web services.
    '''
    if google_api_key:
        os.environ['GOOGLE_API_KEY']=google_api_key
    if here_app_id:
        os.environ['HERE_APP_ID']=here_app_id
    if here_app_code:
        os.environ['HERE_APP_CODE']=here_app_code   


@click.command(help="Start the API server")
@click.option('--service_port')
def proxy(service_port):
    if service_port:
        os.environ['SERVICE_PORT']=service_port
    httpsrv.start()
    return True


@click.command(help="Search for the given address")
@click.argument('address')
def query(address):
    locations = controller.search(address)
    for loc in locations:
        print("{provider}: lat: {lat}, lon: {lon} Address: {addr}".format(
            lat=loc["lat"], lon=loc["lon"], provider=loc["provider"], addr=loc["address"]))
    return True


def main():
    cli()
    return True


cli.add_command(query)
cli.add_command(proxy)

if __name__ == "__main__":
    sys.exit(main())
