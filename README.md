# Zabbix Bulk Website Monitoring

This script allows to add, disable and delete website monitoring in Zabbix.

## Usage

The script accepts the following arguments:

- `action` - Required, can be `add`, `disable` or `delete`  
- `-f, --sites-file` - Path to the file with the list of websites

Example: python zabbix-bulk_script.py add -f sites.txt

This will add monitoring for websites listed in sites.txt file.

## Actions

- `add` - Add new monitoring for websites. Creates Zabbix web scenarios and triggers.

- `disable` - Disable existing monitoring for websites. Disables corresponding web scenarios and triggers.

- `delete` - Completely remove monitoring for websites. Deletes web scenarios and triggers.

## Configuration

The script expects `ZABBIX_SERVER`, `ZABBIX_USER` and `ZABBIX_PASSWORD` environment variables to be set for connecting to Zabbix API.

Default host and application names are used for created entities, but can be modified by changing `ZABBIX_HOST` and `APPLICATION_NAME` constants.

## Logging

The script logs informational and error messages into `zabbix_unified.log` file.

## Requirements

- Python 3.6+
- [pyzabbix](https://github.com/lukecyca/pyzabbix) module
- Access to Zabbix API with permissions to create/update/delete triggers and web scenarios
