import argparse
import sys
import logging
from pyzabbix import ZabbixAPI

# Configure logging
logging.basicConfig(level=logging.INFO,
                    filename='zabbix_unified.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Zabbix API credentials  
ZABBIX_SERVER = 'http://your-zabbix-server.com/'
ZABBIX_USER = 'your-username'
ZABBIX_PASSWORD = 'your-password'

# Default parameters
ZABBIX_HOST = 'your-hostname'
APPLICATION_NAME = 'application-name'

def add_sites(zapi, sites_file):
    
  # Get host ID
  host = zapi.host.get(filter={"host": ZABBIX_HOST})
  if not host:
    raise Exception("Host not found")
  hostid = host[0]["hostid"]

  # Read sites  
  with open(sites_file) as f:
    sites = f.read().splitlines()

  for site in sites:

    scenario_name = f"_{site}"
    
    # Check if scenario exists
    scenario = zapi.httptest.get(filter={"name": scenario_name})
    if scenario:
      logging.info(f"Scenario {scenario_name} already exists")
      continue

    # Get application ID
    application = zapi.application.get(filter={"name": APPLICATION_NAME, "hostid": hostid})
    if not application:
      application = zapi.application.create({"name": APPLICATION_NAME, "hostid": hostid})
      applicationid = application["applicationids"][0]
    else:
      applicationid = application[0]["applicationid"]

    # Create scenario steps
    steps = [
      {
        "name": f"Check {site} via HTTP",
        "url": f"http://{site}",
        "status_codes": "200,301,302",
        "no": 1
      },
      {
        "name": f"Check {site} via HTTPS",
        "url": f"https://{site}", 
        "status_codes": "200,301,302",
        "no": 2  
      }
    ]

    # Create scenario
    scenario = zapi.httptest.create({
      "name": scenario_name,
      "delay": "5",
      "retries": 3,
      "agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36",
      "verify_peer": 1,
      "verify_host": 1,
      "hostid": hostid,
      "applicationid": applicationid,
      "steps": steps
    })

    logging.info(f"Scenario {scenario_name} created")  

    # Create trigger
    trigger_name = f"_Website {site}"
    trigger = zapi.trigger.get(filter={"description": trigger_name})
    if trigger:
      logging.info(f"Trigger {trigger_name} already exists") 
      continue

    trigger = zapi.trigger.create({
      "description": trigger_name,
      "expression": f"{{{ZABBIX_HOST}:web.test.fail[{scenario_name}].min(3m)}}<>0",
      "priority": 4 
    })
    
    logging.info(f"Trigger {trigger_name} created")
  # Get host ID
  host = zapi.host.get(filter={"host": ZABBIX_HOST})
  if not host:
    raise Exception("Host not found")
  hostid = host[0]["hostid"]

  # Read list of sites from file
  with open(sites_file) as f:
    sites = f.read().splitlines()

  # Create web scenario and trigger for each site
  for site in sites:
    scenario_name = f"_{site}"

    # Check if scenario exists
    scenario = zapi.httptest.get(filter={"name": scenario_name})
    if scenario:
      logging.info(f"Scenario {scenario_name} already exists")
      continue

    # Create web scenario
    scenario = zapi.httptest.create({
      "name": scenario_name,
      "delay": "5",
      "retries": 3,
      "agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36",
      "verify_peer": 1,
      "verify_host": 1,
      "hostid": hostid,
      "applicationid": APPLICATION_NAME,
      "steps": steps,
    })

    logging.info(f"Scenario {scenario_name} created")

    # Create trigger
    trigger_name = f"_Website {site}"
    trigger = zapi.trigger.get(filter={"description": trigger_name})
    if trigger:
      logging.info(f"Trigger {trigger_name} already exists")
      continue

    trigger = zapi.trigger.create({
      "description": trigger_name,
      "expression": f"{{{ZABBIX_HOST}:web.test.fail[{scenario_name}].min(3m)}}<>0",
      "priority": 4,
    })

    logging.info(f"Trigger {trigger_name} created")

  # Get host ID
  host = zapi.host.get(filter={"host": ZABBIX_HOST})
  if not host:
    raise Exception("Host not found")
  hostid = host[0]["hostid"]

  # Read list of sites from file
  with open(sites_file) as f:
    sites = f.read().splitlines()

  # Create web scenario and trigger for each site
  for site in sites:
    scenario_name = f"_{site}"

    # Check if scenario exists
    scenario = zapi.httptest.get(filter={"name": scenario_name})
    if scenario:
      logging.info(f"Scenario {scenario_name} already exists")
      continue

    # Create web scenario
    scenario = zapi.httptest.create({
      "name": scenario_name,
      "delay": "5",
      "retries": 3,
      "agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36",
      "verify_peer": 1,
      "verify_host": 1,
      "hostid": hostid,
      "applicationid": APPLICATION_NAME,
      "steps": steps,
    })

    logging.info(f"Scenario {scenario_name} created")

    # Create trigger
    trigger_name = f"_Website {site}"
    trigger = zapi.trigger.get(filter={"description": trigger_name})
    if trigger:
      logging.info(f"Trigger {trigger_name} already exists")
      continue

    trigger = zapi.trigger.create({
      "description": trigger_name,
      "expression": f"{{{ZABBIX_HOST}:web.test.fail[{scenario_name}].min(3m)}}<>0",
      "priority": 4,
    })

    logging.info(f"Trigger {trigger_name} created")
  """
  Add monitoring for websites listed in sites file.
  Creates web scenario and trigger for each site.
  """

  # Get host ID
  host = zapi.host.get(filter={"host": ZABBIX_HOST})
  if not host:
    raise Exception("Host not found")
  hostid = host[0]["hostid"]

  # Read list of sites from file
  with open(sites_file) as f:
    sites = f.read().splitlines()

  # Create web scenario and trigger for each site
  for site in sites:
    scenario_name = f"_{site}"
    
    # Check if scenario exists
    scenario = zapi.httptest.get(filter={"name": scenario_name})
    if scenario:
      logging.info(f"Scenario {scenario_name} already exists")
      continue

    # Get application ID  
    application = zapi.application.get(filter={"name": APPLICATION_NAME, "hostid": hostid})
    if not application:
      application = zapi.application.create({"name": APPLICATION_NAME, "hostid": hostid})
      applicationid = application["applicationids"][0]
    else:
      applicationid = application[0]["applicationid"]

    # Create web scenario
    scenario = zapi.httptest.create({
      "name": scenario_name,
      "delay": "5", 
      "retries": 3,
      "agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36",
      "verify_peer": 1,
      "verify_host": 1,
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
    
    logging.info(f"Scenario {scenario_name} created")

    # Create trigger
    trigger_name = f"_Website {site}"
    trigger = zapi.trigger.get(filter={"description": trigger_name})
    if trigger:
      logging.info(f"Trigger {trigger_name} already exists")
      continue

    trigger = zapi.trigger.create({
      "description": trigger_name,
      "expression": f"{{{ZABBIX_HOST}:web.test.fail[{scenario_name}].min(3m)}}<>0",  
      "priority": 4 
    })
    
    logging.info(f"Trigger {trigger_name} created")
        
def disable_sites(zapi, sites_file):
  """
  Disable monitoring for websites listed in sites file.
  Disables web scenarios and triggers.
  """
  
  with open(sites_file) as f:
    sites = f.read().splitlines()

  for site in sites:

    scenario = zapi.httptest.get(filter={"name": f"_{site}"})
    if scenario:
      zapi.httptest.update({"httptestid": scenario[0]["httptestid"], "status": 1})
      logging.info(f"Scenario {site} disabled")

    trigger = zapi.trigger.get(filter={"description": f"_Website {site}"})
    if trigger:
      zapi.trigger.update({"triggerid": trigger[0]["triggerid"], "status": 1})
      logging.info(f"Trigger {site} disabled")
      
def delete_sites(zapi, sites_file):
  """
  Delete monitoring for websites listed in sites file.
  Deletes web scenarios and triggers.
  """

  with open(sites_file) as f:
    sites = f.read().splitlines()

  for site in sites:
  
    scenario = zapi.httptest.get(filter={"name": f"_{site}"})
    if scenario:
      zapi.httptest.delete(scenario[0]["httptestid"])
      logging.info(f"Deleted scenario {site}")

    trigger = zapi.trigger.get(filter={"description": f"_Website {site}"})
    if trigger:
      zapi.trigger.delete(trigger[0]["triggerid"])
      logging.info(f"Deleted trigger {site}")

def main():
    
  parser = argparse.ArgumentParser()
  
  parser.add_argument("action", choices=["add", "disable", "delete"])
  
  parser.add_argument("-f", "--sites-file")
  
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)
    
  args = parser.parse_args()
  
  if not args.sites_file:
    print("Sites file parameter is required")
    sys.exit(1)  

  zapi = ZabbixAPI(ZABBIX_SERVER)
  zapi.login(ZABBIX_USER, ZABBIX_PASSWORD)

  if args.action == "add":
    add_sites(zapi, args.sites_file)
  elif args.action == "disable":
    disable_sites(zapi, args.sites_file)
  elif args.action == "delete":  
    delete_sites(zapi, args.sites_file)
  
  logging.info("Script finished")

if __name__ == "__main__":
  main()
