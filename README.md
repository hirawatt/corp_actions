# Corporate Actions from NSE India

## Setup
- Run `pip install -r requirements.txt`
- Create a .env file with the following content
```
discord_webhook_url=<discord_webhook_url>
```
> Replace <discord_webhook_url> with the respective webhook url.
- Run `python3 main.py` from the project home folder.
- [Optional] Setup cronjob setup for Linux systems for running this script automatically everyday at 7 pm.
```
0 19 * * * /usr/bin/python3 /localtion/to/this/repo/main.py
```
> Add the code above to you cronjob setup file using `crontab -e`
>
> Use `crontab -l` to check for you cronjobs file.

## Data Source
- https://www1.nseindia.com/corporates/corporateHome.html
- https://www.nseindia.com/all-reports

## Known Issues
- Large data cannot be sent to Discord server using Webhooks
-
