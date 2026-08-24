def get_hosts_ids(hostnames: str | list[str], search_linux: bool = False) -> tuple[str, dict]:
    variables = {
        "hostRoot": "WINDOWS_HOST_ROOT" if not search_linux else "LINUX_HOST_ROOT",
        "filter": [
            {
                "field": "NAME",
                "texts": hostnames if isinstance(hostnames, str) else [hostnames]
            },
            {
                "field": "IS_RELIC",
                "texts": [
                    "false"
                ]
            },
            {
                "field": "IS_REPLICATED",
                "texts": [
                    "false"
                ]
            },
            {
                "field": "IS_KUPR_HOST",
                "texts": [
                    "false"
                ]
            }
        ],
        "sortBy": "NAME",
        "sortOrder": "ASC"
    }

    query = """query PhysicalHostListQuery($hostRoot: HostRoot!,
      $sortBy: HierarchySortByField,
      $sortOrder: SortOrder, 
      $filter: [Filter!]!) {
      physicalHosts(
        hostRoot: $hostRoot
        filter: $filter
        sortBy: $sortBy
        sortOrder: $sortOrder
      ) {
        nodes {
          id
          name
          osType
        }
      }
    }
    """

    return query, variables


def update_certificate_for_host(host_id: str) -> tuple[str, dict]:
    variables = {
        "hostUpdateProperties": [
            {
                "hostId": host_id,
                "updateProperties": {
                    "isUpdateCertAndAgentIdEnabled": True
                }
            }
        ]
    }

    query = """mutation EditPhysicalHostMutation($hostUpdateProperties: [HostUpdateIdInput!]!) {
      bulkUpdateHost(input: {
        hostUpdateProperties: $hostUpdateProperties
      }) {
        output {
          items {
            hostSummary {
              id
              name
              agentId
            }
          }
        }
      }
    }"""

    return query, variables
