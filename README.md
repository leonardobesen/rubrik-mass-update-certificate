# rubrik-mass-update-certificate

If you've ever had to update certificates for 100+ hosts, you know how painful and time-consuming it can be. So, instead of wasting 20 minutes of my precious time updating each certificate manually, I spent an hour writing this script to do it for me. Then spent 30 more minutes to have it completely refactored by AI.

Now you can use it too!... In case you just happened to be browsing GitHub for a script that does exactly this. How likely that is, I wouldn’t know.

## Dependencies

- Python >= 3.12
- Install dependencies:

```bash
pip install -r requirements.txt
```

## How to use it

1. Create a JSON file named `config.json` with your Rubrik Security Cloud (RSC) and service account information and place it inside the `configuration` folder.

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

2. Clone this repository to a machine with network access to your Rubrik RSC.

3. Create a CSV file with hostnames (one per row) — the script reads the first column and will skip common header names (`hostname`, `host`, `name`).

4. You can run the script in dry-run mode to verify host resolution without changing anything:

```bash
python main.py --csv path/to/hosts.csv --dry-run
```

5. To actually perform the updates and produce a report:

```bash
python main.py --csv path/to/hosts.csv
```

### Notes

- The script resolves hostnames for both Windows and Linux roots and deduplicates host ids before performing the update.
- Use `--dry-run` to validate the CSV and see which host ids would be updated.

If you want help adding unit tests or CI for this project, I can scaffold a simple `pytest` suite.
