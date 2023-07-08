from pyzabbix import ZabbixAPI

ZABBIX_SERVER = 'http://your-zabbix-server.com/'
ZABBIX_USER = 'your-username'
ZABBIX_PASSWORD = 'your-password'
ZABBIX_HOST = 'your-hostname'
APPLICATION_NAME = 'application-name'
SITES_FILE = 'sites-list'

# Connect to Zabbix API
zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.login(ZABBIX_USER, ZABBIX_PASSWORD)

# Get host ID
host = zapi.host.get(filter={"host": ZABBIX_HOST})
if not host:
    raise Exception("Host not found")
hostid = host[0]["hostid"]

# Read list of sites from file
with open(SITES_FILE, 'r') as f:
    sites = f.read().splitlines()

# Create web scenario and trigger for each site
for site in sites:
    scenario_name = f"_{site}"
    
    # Check if scenario with given name already exists
    scenario = zapi.httptest.get(filter={"name": scenario_name})
    if scenario:
        print(f"Web scenario '{scenario_name}' already exists")
        continue
    
    # Get application ID
    application = zapi.application.get(filter={"name": APPLICATION_NAME, "hostid": hostid})
    if not application:
        print(f"Application '{APPLICATION_NAME}' not found, creating it")
        application = zapi.application.create({
            "name": APPLICATION_NAME,
            "hostid": hostid
        })
        applicationid = application["applicationids"][0]
    else:
        applicationid = application[0]["applicationid"]
    
    # Create web scenario
    scenario = zapi.httptest.create({
        "name": scenario_name,
        "delay": "5", # Check interval (in seconds)
        "retries": 3, # Number of attempts to perform web scenario steps
        "agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36", # User agent string
        "verify_peer": 1, # Enable SSL certificate verification
        "verify_host": 1, # Enable hostname verification
        "hostid": hostid,
        "applicationid": applicationid,
        "steps": [
            {
                "name": f"Check {site} via HTTP",
                "url": f"http://{site}",
                "status_codes": "200,301,302",
                "required": site,
                "no": 1
            },
            {
                "name": f"Check {site} via HTTPS",
                "url": f"https://{site}",
                "status_codes": "200,301,302",
                "required": site,
                "no": 2
            }
        ]
    })
    
    print(f"Web scenario '{scenario_name}' created successfully")
    
    trigger_name = f"_Website {site}"
    
    # Check if trigger with given name already exists
    trigger = zapi.trigger.get(filter={"description": trigger_name})
    if trigger:
        print(f"Trigger '{trigger_name}' already exists")
        continue
    
    # Create trigger for web scenario
    trigger = zapi.trigger.create({
        "description": trigger_name,
        "expression": f"{{{ZABBIX_HOST}:web.test.fail[{scenario_name}].min(3m)}}<>0",
        "priority": 4 # Trigger severity (4 - high)
    })
    
    print(f"Trigger '{trigger_name}' created successfully")
