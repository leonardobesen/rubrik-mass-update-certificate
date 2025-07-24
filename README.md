# rubrik-mass-update-certificate

If you've ever had to update certificates for 100+ hosts, you know how painful and time-consuming it can be. So, instead of wasting 20 minutes of my precious time updating each certificate manually, I spent an hour writing this script to do it for me.

Now you can use it too!... In case you just happened to be browsing GitHub for a script that does exactly this. How likely that is, I wouldn’t know.

## Dependencies

- Python >= 3.12.5
- tqdm
- requests
- pandas

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
