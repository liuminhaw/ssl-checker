# ssl-checker
Check for websites SSL certificates expiration date

## Version 0.1.0
- Check ssl expiration mail for websites
- Set different recipient for different sites
- `sendgrid` method to send notification mail

### Configuration
- `conf.json`: General settings
- `sites.json`: Sites information for ssl check

### Usage
```
python3 check.py
```

### Error Codes
- `1` : configuration file missing
- `11` : checker_conf.configError - configuration settings error 