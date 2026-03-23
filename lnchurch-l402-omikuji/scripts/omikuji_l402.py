#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
from pathlib import Path

import requests
import urllib3

urllib3.disable_warnings()


def eprint(*args):
    print(*args, file=sys.stderr)


def load_macaroon_hex(path: str) -> str:
    return Path(path).expanduser().read_bytes().hex()


def get_json(url: str, **kwargs):
    r = requests.get(url, timeout=30, **kwargs)
    r.raise_for_status()
    return r.json()


def post(url: str, **kwargs):
    return requests.post(url, timeout=30, **kwargs)


def parse_www_authenticate(header: str) -> tuple[str, str]:
    m1 = re.search(r'macaroon="([^"]+)"', header)
    m2 = re.search(r'invoice="([^"]+)"', header)
    if not (m1 and m2):
        raise ValueError('Failed to parse WWW-Authenticate header')
    return m1.group(1), m2.group(1)


def lnd_rest_pay_invoice(rest_url: str, tls_cert: str, macaroon_hex: str, invoice: str, fee_limit_sat: int, timeout_seconds: int) -> dict:
    url = rest_url.rstrip('/') + '/v2/router/send'
    payload = {
        'payment_request': invoice,
        'fee_limit_sat': fee_limit_sat,
        'timeout_seconds': timeout_seconds,
    }
    r = requests.post(
        url,
        headers={'Grpc-Metadata-macaroon': macaroon_hex},
        json=payload,
        verify=tls_cert,
        timeout=timeout_seconds + 10,
        stream=True,
    )
    r.raise_for_status()

    last = None
    for line in r.iter_lines():
        if not line:
            continue
        last = json.loads(line)
        result = last.get('result', {})
        status = result.get('status')
        if status == 'SUCCEEDED':
            return result
        if status == 'FAILED':
            raise RuntimeError(json.dumps(last, ensure_ascii=False))

    raise RuntimeError(f'No terminal payment status received: {last}')


def main():
    ap = argparse.ArgumentParser(description='Execute LN Church Omikuji over L402 using lnd REST.')
    ap.add_argument('--agent-id', required=True)
    ap.add_argument('--probe-source', default='openclaw-skill')
    ap.add_argument('--api-base', default='https://kari.mayim-mayim.com')
    ap.add_argument('--max-cost', type=int, default=10)
    ap.add_argument('--fee-limit-sat', type=int, default=1)
    ap.add_argument('--timeout-seconds', type=int, default=30)
    ap.add_argument('--lnd-rest-url', default=os.getenv('LND_REST_URL', 'https://localhost:8080'))
    ap.add_argument('--lnd-tls-cert', default=os.getenv('LND_TLS_CERT', str(Path.home() / '.lnd/tls.cert')))
    ap.add_argument('--lnd-macaroon-file', default=os.getenv('LND_MACAROON_FILE', str(Path.home() / '.lnd/data/chain/bitcoin/mainnet/admin.macaroon')))
    ap.add_argument('--show-sensitive', action='store_true', help='Include sensitive values such as probe_token, invoice, and payment_preimage in output.')
    ap.add_argument('--insecure', action='store_true', help='Disable TLS verification for LN Church API calls only.')
    args = ap.parse_args()

    verify_api = False if args.insecure else True
    omikuji_url = args.api_base.rstrip('/') + '/api/agent/omikuji'
    probe_url = args.api_base.rstrip('/') + '/api/agent/probe'

    probe1 = get_json(probe_url, params={'src': args.probe_source, 'agentId': args.agent_id}, verify=verify_api)
    probe2 = get_json(probe1['next_action']['url'], verify=verify_api)
    probe_token = probe2['capability_receipt']['token']

    payload = {
        'agentId': args.agent_id,
        'clientType': 'AI',
        'scheme': 'L402',
        'asset': 'SATS',
    }
    base_headers = {
        'Content-Type': 'application/json',
        'x-probe-token': probe_token,
    }

    initial = post(omikuji_url, headers=base_headers, json=payload, verify=verify_api)
    if initial.status_code != 402:
        initial.raise_for_status()
        raise RuntimeError(f'Expected 402, got {initial.status_code}: {initial.text}')

    challenge = initial.json()
    amount = int(challenge['challenge']['amount'])
    if amount > args.max_cost:
        raise RuntimeError(f'Challenge amount {amount} SATS exceeds max-cost {args.max_cost} SATS')

    www_auth = initial.headers.get('WWW-Authenticate', '')
    l402_macaroon, invoice = parse_www_authenticate(www_auth)

    pay_result = lnd_rest_pay_invoice(
        args.lnd_rest_url,
        args.lnd_tls_cert,
        load_macaroon_hex(args.lnd_macaroon_file),
        invoice,
        args.fee_limit_sat,
        args.timeout_seconds,
    )
    preimage = pay_result['payment_preimage']

    settled_headers = dict(base_headers)
    settled_headers['Authorization'] = f'L402 {l402_macaroon}:{preimage}'
    final = post(omikuji_url, headers=settled_headers, json=payload, verify=verify_api)
    final.raise_for_status()

    output = {
        'challenge_amount_sat': amount,
        'payment': {
            'status': pay_result.get('status'),
            'payment_hash': pay_result.get('payment_hash'),
            'fee_sat': pay_result.get('fee_sat'),
        },
        'omikuji': final.json(),
    }
    if args.show_sensitive:
        output['probe_token'] = probe_token
        output['invoice'] = invoice
        output['payment']['payment_preimage'] = preimage
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
