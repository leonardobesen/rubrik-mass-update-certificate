from typing import List
from connection.wrapper import request
from graphql import queries


def get_host_ids(access_token: str, hostname: str) -> List[str]:
    """Query Rubrik for host ids matching `hostname` for Windows and Linux."""
    ids: List[str] = []
    for search_linux in (False, True):
        query, variables = queries.get_hosts_ids(hostname, search_linux=search_linux)
        response = request(access_token, query, variables)
        nodes = response.get("data", {}).get("physicalHosts", {}).get("nodes", [])
        for node in nodes:
            node_id = node.get("id")
            if node_id and node_id not in ids:
                ids.append(node_id)
    return ids


def update_certificate(access_token: str, host_id: str) -> dict:
    """Perform the certificate update mutation for a given host id."""
    query, variables = queries.update_certificate_for_host(host_id)
    return request(access_token, query, variables)
