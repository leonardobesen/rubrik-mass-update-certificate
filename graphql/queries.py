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

    query = f"""mutation EditPhysicalHostMutation($hostUpdateProperties: [HostUpdateIdInput!]!) {{
      bulkUpdateHost(input: {{hostUpdateProperties: $hostUpdateProperties}}) {{
        output {{
          items {{
            hostSummary {{
              id
              name
              agentId
            }}
          }}
        }}
      }}
    }}"""

    return query, variables
