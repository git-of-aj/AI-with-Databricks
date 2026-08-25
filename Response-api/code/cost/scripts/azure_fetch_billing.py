import requests
import time
from datetime import datetime


# ============================================================
# Azure credentials
# ============================================================

subscription_id = 'xxxxxxxxxxxxxxxx'
tenant_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
client_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
client_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# ============================================================
# Configuration
# ============================================================

monthly_budget = 500000  # INR

MAX_RETRIES = 6

INITIAL_RETRY_SECONDS = 5


# ============================================================
# Dates
# ============================================================

now = datetime.now()

start_of_year = datetime(2026, 1, 1)

start_of_year_str = start_of_year.strftime(
    '%Y-%m-%dT00:00:00Z'
)

today_str = now.strftime(
    '%Y-%m-%dT23:59:59Z'
)


# ============================================================
# Authenticate with Azure AD
# ============================================================

auth_url = (
    f'https://login.microsoftonline.com/'
    f'{tenant_id}/oauth2/token'
)

auth_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'resource': 'https://management.azure.com/'
}

try:

    auth_response = requests.post(
        auth_url,
        data=auth_data,
        timeout=30
    )

    auth_response.raise_for_status()

except requests.exceptions.RequestException as e:

    print(
        f"ERROR: Azure authentication failed: {e}"
    )

    exit(1)


auth_json = auth_response.json()

if 'access_token' not in auth_json:

    print(
        "ERROR: Azure did not return an access token."
    )

    print(auth_json)

    exit(1)


access_token = auth_json['access_token']


# ============================================================
# Azure Cost Management API
# ============================================================

usage_url = (
    f'https://management.azure.com/subscriptions/'
    f'{subscription_id}/providers/Microsoft.CostManagement/query'
    f'?api-version=2019-11-01'
)


# ============================================================
# IMPORTANT HEADERS
#
# X-Ms-Command-Name: CostAnalysis
# ============================================================

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
    'X-Ms-Command-Name': 'CostAnalysis'
}


# ============================================================
# Function to query Azure Cost Management
#
# Includes retry handling for HTTP 429.
# ============================================================

def query_cost_management(query_data):

    for attempt in range(1, MAX_RETRIES + 1):

        try:

            response = requests.post(
                usage_url,
                headers=headers,
                json=query_data,
                timeout=120
            )

        except requests.exceptions.RequestException as e:

            if attempt == MAX_RETRIES:

                print(
                    f"ERROR: Request failed after "
                    f"{MAX_RETRIES} attempts."
                )

                print(e)

                return None

            retry_seconds = (
                INITIAL_RETRY_SECONDS
                * (2 ** (attempt - 1))
            )

            print(
                f"Request failed: {e}"
            )

            print(
                f"Retrying in "
                f"{retry_seconds} seconds..."
            )

            time.sleep(retry_seconds)

            continue


        # ====================================================
        # Successful response
        # ====================================================

        if response.status_code == 200:

            return response


        # ====================================================
        # Rate limited - HTTP 429
        # ====================================================

        if response.status_code == 429:

            retry_after = (
                response.headers.get(
                    'x-ms-ratelimit-microsoft.consumption-retry-after'
                )
            )

            # Also check standard Retry-After header
            if not retry_after:

                retry_after = (
                    response.headers.get(
                        'Retry-After'
                    )
                )


            # Use Azure's retry value if available
            if retry_after:

                try:

                    retry_seconds = float(
                        retry_after
                    )

                except ValueError:

                    retry_seconds = (
                        INITIAL_RETRY_SECONDS
                        * (2 ** (attempt - 1))
                    )

            else:

                retry_seconds = (
                    INITIAL_RETRY_SECONDS
                    * (2 ** (attempt - 1))
                )


            print()

            print(
                f"Azure returned HTTP 429 "
                f"(Too Many Requests)."
            )

            print(
                f"Retry attempt "
                f"{attempt}/{MAX_RETRIES}"
            )

            print(
                f"Waiting {retry_seconds:.0f} "
                f"seconds before retry..."
            )

            if attempt < MAX_RETRIES:

                time.sleep(retry_seconds)

                continue

            else:

                print(
                    "ERROR: Azure rate limit "
                    "was not cleared."
                )

                print()
                print("Azure response:")

                print(response.text)

                return None


        # ====================================================
        # Service unavailable - HTTP 503
        # ====================================================

        if response.status_code == 503:

            if attempt < MAX_RETRIES:

                retry_seconds = (
                    INITIAL_RETRY_SECONDS
                    * (2 ** (attempt - 1))
                )

                print(
                    "Azure returned HTTP 503."
                )

                print(
                    f"Retrying in "
                    f"{retry_seconds} seconds..."
                )

                time.sleep(retry_seconds)

                continue

            else:

                print(
                    "ERROR: Azure service "
                    "is unavailable."
                )

                print(response.text)

                return None


        # ====================================================
        # Other HTTP errors
        # ====================================================

        print(
            f"ERROR: Azure returned "
            f"HTTP {response.status_code}"
        )

        print()
        print("Azure response:")
        print(response.text)

        return None


    return None


# ============================================================
# YEAR-TO-DATE QUERY
#
# January 1, 2026 -> Today
#
# Aggregated by ServiceName
# ============================================================

year_to_date_data = {

    'type': 'Usage',

    'timeframe': 'Custom',

    'timePeriod': {

        'from': start_of_year_str,

        'to': today_str

    },

    'dataset': {

        # We only need one aggregated value per service.
        'granularity': 'None',

        'aggregation': {

            'totalCost': {

                'name': 'Cost',

                'function': 'Sum'

            }

        },

        'grouping': [

            {

                'type': 'Dimension',

                'name': 'ServiceName'

            }

        ]

    }

}


# ============================================================
# CURRENT MONTH QUERY
# ============================================================

start_of_month = datetime(
    now.year,
    now.month,
    1
)

start_of_month_str = start_of_month.strftime(
    '%Y-%m-%dT00:00:00Z'
)


monthly_data = {

    'type': 'Usage',

    'timeframe': 'Custom',

    'timePeriod': {

        'from': start_of_month_str,

        'to': today_str

    },

    'dataset': {

        'granularity': 'None',

        'aggregation': {

            'totalCost': {

                'name': 'Cost',

                'function': 'Sum'

            }

        },

        'grouping': [

            {

                'type': 'Dimension',

                'name': 'ServiceName'

            }

        ]

    }

}


# ============================================================
# Query YEAR-TO-DATE
# ============================================================

print()
print("Fetching year-to-date Azure costs...")
print(
    f"Period: "
    f"{start_of_year.strftime('%Y-%m-%d')} "
    f"to "
    f"{now.strftime('%Y-%m-%d')}"
)
print()


ytd_response = query_cost_management(
    year_to_date_data
)


if ytd_response is None:

    print(
        "ERROR: Unable to retrieve "
        "year-to-date cost data."
    )

    exit(1)


# ============================================================
# Query CURRENT MONTH
# ============================================================

print(
    "Fetching current-month Azure costs..."
)

monthly_response = query_cost_management(
    monthly_data
)


if monthly_response is None:

    print(
        "ERROR: Unable to retrieve "
        "monthly cost data."
    )

    exit(1)


# ============================================================
# Parse YTD response
# ============================================================

try:

    ytd_json = ytd_response.json()

    ytd_rows = (
        ytd_json
        .get('properties', {})
        .get('rows', [])
    )

except ValueError:

    print(
        "ERROR: Azure returned invalid "
        "JSON for YTD query."
    )

    print(ytd_response.text)

    exit(1)


# ============================================================
# Parse monthly response
# ============================================================

try:

    monthly_json = monthly_response.json()

    monthly_rows = (
        monthly_json
        .get('properties', {})
        .get('rows', [])
    )

except ValueError:

    print(
        "ERROR: Azure returned invalid "
        "JSON for monthly query."
    )

    print(monthly_response.text)

    exit(1)


# ============================================================
# Process YTD services
#
# Expected Azure row:
#
# [Cost, ServiceName, Currency]
# ============================================================

ytd_services = []


for row in ytd_rows:

    if len(row) < 3:

        continue


    try:

        cost = float(row[0])

    except (ValueError, TypeError):

        continue


    service = row[1]

    currency = row[2]


    ytd_services.append({

        'service': service,

        'cost': cost,

        'currency': currency

    })


# ============================================================
# Sort YTD services
# ============================================================

ytd_services_sorted = sorted(

    ytd_services,

    key=lambda x: x['cost'],

    reverse=True

)


# ============================================================
# Calculate YTD total
# ============================================================

total_ytd_cost = sum(

    service['cost']

    for service in ytd_services

)


# ============================================================
# Determine currency
# ============================================================

currency = 'N/A'


if ytd_services:

    currency = ytd_services[0]['currency']


# ============================================================
# Process monthly services
# ============================================================

monthly_services = []


for row in monthly_rows:

    if len(row) < 3:

        continue


    try:

        cost = float(row[0])

    except (ValueError, TypeError):

        continue


    monthly_services.append({

        'service': row[1],

        'cost': cost,

        'currency': row[2]

    })


# ============================================================
# Calculate monthly total
# ============================================================

total_monthly_cost = sum(

    service['cost']

    for service in monthly_services

)


# ============================================================
# Calculate budget percentage
# ============================================================

if monthly_budget > 0:

    percent_consumed = (

        total_monthly_cost

        / monthly_budget

    ) * 100

else:

    percent_consumed = 0


# ============================================================
# PRINT REPORT
# ============================================================

print()

print("=" * 65)

print(
    "                    AZURE COST REPORT"
)

print("=" * 65)

print()

print(
    f"Report generated: "
    f"{now.strftime('%Y-%m-%d %H:%M:%S')}"
)

print(
    f"Cost period: "
    f"{start_of_year.strftime('%Y-%m-%d')} "
    f"to "
    f"{now.strftime('%Y-%m-%d')}"
)

print()


# ============================================================
# YTD COST
# ============================================================

print("-" * 65)

print("YEAR-TO-DATE COST")

print("-" * 65)

print(

    f"Total cost since "
    f"{start_of_year.strftime('%Y-%m-%d')}: "
    f"{total_ytd_cost:,.2f} {currency}"

)

print()


# ============================================================
# TOP 5 SERVICES
# ============================================================

print("-" * 65)

print("TOP 5 SERVICES BY COST")

print("-" * 65)


if ytd_services_sorted:

    for i, service in enumerate(

        ytd_services_sorted[:5],

        start=1

    ):

        print(

            f"{i}. "
            f"{service['service']} - "
            f"{service['cost']:,.2f} "
            f"{service['currency']}"

        )

else:

    print(
        "No service cost data returned by Azure."
    )


print()


# ============================================================
# CURRENT MONTH
# ============================================================

print("-" * 65)

print("CURRENT MONTH")

print("-" * 65)

print(

    f"Total cost for "
    f"{now.strftime('%B %Y')}: "
    f"{total_monthly_cost:,.2f} "
    f"{currency}"

)

print(

    f"Monthly budget: "
    f"{monthly_budget:,.2f} INR"

)

print(

    f"Percentage of monthly budget consumed: "
    f"{percent_consumed:.2f}%"

)

print()


# ============================================================
# API INFORMATION
# ============================================================

print("-" * 65)

print("API INFORMATION")

print("-" * 65)

print(
    "Command header: X-Ms-Command-Name: CostAnalysis"
)

print(
    f"YTD rows returned: {len(ytd_rows)}"
)

print(
    f"Monthly rows returned: {len(monthly_rows)}"
)

print()


# ============================================================
# END
# ============================================================

print("=" * 65)

print(
    "Report completed successfully."
)

print("=" * 65)

print()
