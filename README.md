# rubrik-mass-update-certificate

If ever had to update certificate for 100+ hosts you know how painful and waste of time it is. So, instead of spending 20 minutes of my precious time updating the certificate of 100 or so hosts I spent 1 hour making this script to do that for me. Now you can use that too, if by any chance you were browsing GitHub for a script that does that, however likely this situation is I wouldn't know.

## Dependencies

- Python >= 3.12.5
- tqdm

## How to use it

1- Create a JSON file named `config.json` with your Rubrik Security Cloud (RSC) and RSC Service Account information like in the example below and add it inside `configuration` folder:

```json
```json
{
 "client_id": "your_client_id",
 "client_secret": "your_client_secret",
 "name": "name_you_gave",
 "access_token_uri": "https://yourdomain.my.rubrik.com/api/client_token",
 "graphql_url": "https://yourdomain.my.rubrik.com/api/graphql"
 "client_id": "your_client_id",
 "client_secret": "your_client_secret",
 "name": "name_you_gave",
 "access_token_uri": "https://yourdomain.my.rubrik.com/api/client_token",
 "graphql_url": "https://yourdomain.my.rubrik.com/api/graphql"
}
```

3- Download this repository and place in a computer or server that has access to your Rubrik RSC.

4- Create a CSV files named `host_ids.csv` (with just 1 column and without headers).

5- Add to `host_ids.csv` all the host ids of the hosts you want to execute this command. You may use this GraphQL query on your RSC playground to easy get that list:
3- Download this repository and place in a computer or server that has access to your Rubrik RSC.

4- Create a CSV files named `host_ids.csv` (with just 1 column and without headers).

5- Add to `host_ids.csv` all the host ids of the hosts you want to execute this command. You may use this GraphQL query on your RSC playground to easy get that list:

```graphql
query PhysicalHostListQuery($hostRoot: HostRoot!,
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
    }
  }
}
```

Parameters:

```json
{
  "hostRoot": "LINUX_HOST_ROOT",
  "filter": [
    {
      "field": "CLUSTER_ID",
      "texts": [
        "YOUR CLUSTER UUID HERE"
      ]
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
      "field": "PHYSICAL_HOST_CONNECTION_STATUS",
      "texts": [
        "Disconnected"
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
  "sortOrder": "ASC",
  "childFilter": [
    {
      "field": "IS_GHOST",
      "texts": [
        "false"
      ]
    },
    {
      "field": "IS_RELIC",
      "texts": [
        "false"
      ]
    }
  ]
}
```

4- Run main.py
