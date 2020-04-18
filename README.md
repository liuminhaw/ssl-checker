# ssl-checker
Check for websites SSL certificates expiration date

## Version 0.1.1
- Show `version` option
- Update logger module (Daily logs)
- Update log format 

Version 0.1.0
- Check ssl expiration mail for websites
- Set different recipient for different sites
- `sendgrid` method to send notification mail

### Configuration
- `conf.json`: General settings
- `sites.json`: Sites information for ssl check

### Usage
```
usage: checker.py [-h] [-V]

optional arguments:
  -h, --help     show this help message and exit
  -V, --version  show program's version number and exit
```

### Error Codes
- `1` : configuration file missing
- `11` : checker_conf.configError - configuration settings error 