import argparse
import json

from requests import Session, Response
from typing import Optional, Generator


def login(session: Session, domain: str, username: str, password: str, proxies: Optional[dict] = None) -> None:
    # login
    extra_headers: dict = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body_params: dict = {
        'username': username,
        'password': password,
    }
    try:
        resp_login: Response = session.post(
            url=f'https://{domain}/login',
            data=body_params,
            headers=extra_headers,
            proxies=proxies,
        )
        resp_login.raise_for_status()
        print(f'\n\nLogin response:\n{resp_login}\n\n')
    except Exception as exc_login:
        raise exc_login


def main(domain: str, username: str, password: str, proxies: Optional[dict] = None) -> Generator[dict, None, None]:
    try:
        session = Session()

        login(session=session, domain=domain, username=username, password=password, proxies=proxies)

        # get devices
        headers: dict = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        url_params: dict = {
            'page': 1,
            'page_size': 1,
        }

        resp_results: Response = session.get(
            url=f'https://{domain}/api/pool',
            params=url_params,
            headers=headers,
            proxies=proxies,
        )
        resp_results.raise_for_status()
        data_entity: dict = resp_results.json()
        results: list = data_entity.get('results')
        if not results:
            print(f'\n\nDevices response:\n{resp_results}\n\n')
        for result in results:
            yield result
    except Exception as exc_results:
        raise exc_results


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--username',
            type=str,
            help='The username',
            required=True,
            default=None
        )
        parser.add_argument(
            '--password',
            type=str,
            help='The password',
            required=True,
            default=None
        )
        parser.add_argument(
            '--domain',
            type=str,
            help="The FQDN for your AVI device",
            required=True,
        )
        parser.add_argument(
            '--proxies',
            type=str,
            help="JSON structure specifying 'http' and 'https' proxy URLs",
            required=False,
        )
        args = parser.parse_args()

        proxies: Optional[dict] = None
        if args.proxies:
            proxies = json.loads(args.proxies)

        for device in main(
            domain=args.domain,
            username=args.username,
            password=args.password,
            proxies=proxies,
        ):
            print(f'device info: {device}')
        print('End of devices')
    except Exception as exc_main:
        print(f'{exc_main}')
