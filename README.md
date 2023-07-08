# Zabbix Bulk Website Monitoring

This script is written in Python and uses the PyZabbix library to interact with the Zabbix API. It logs into a Zabbix server, reads a list of websites from a file specified in the `SITES_FILE` variable, and creates a web scenario and trigger for each website to monitor their availability via HTTP and HTTPS. If the application with the specified name is not found, the script automatically creates it.

## Variables

The script uses the following variables:
- `ZABBIX_SERVER`: The URL of the Zabbix server.
- `ZABBIX_USER`: The username for logging into Zabbix.
- `ZABBIX_PASSWORD`: The password for logging into Zabbix.
- `ZABBIX_HOST`: The hostname of the host you want to monitor.
- `APPLICATION_NAME`: The name of the application to be used for the created web scenarios.
- `SITES_FILE`: The name of the file containing the list of websites to monitor.

## Requirements

To run this script, Python 3 and the PyZabbix library must be installed.

## Usage

1. Replace the values of the variables `ZABBIX_SERVER`, `ZABBIX_USER`, `ZABBIX_PASSWORD`, `ZABBIX_HOST`, `APPLICATION_NAME`, and `SITES_FILE` with the appropriate values for your Zabbix server and the file containing the list of websites to monitor.
2. Create a file with the name specified in the `SITES_FILE` variable and add the list of websites you want to monitor, one per line.
3. Run the script using Python 3.
