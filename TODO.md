# TODO

## Next Steps:

1. Define the status of services (OK and ERROR enough?)
2. Handle the status of services and produce a new internal status (OK, ERROR, WARNING enough?)
3. Implement the Task interface and write a task to store output in a database
4. Implement the Plugin interface and write a plugin to show some data and statistics in a web interface
5. Add more services, tasks and maybe plugins...

## Things to do in no particular order:

- Implement error handling at all needed places! currently nearly no error handling is done!
- Configure the logger
- Make use of the logger wherever it us useful! and be informative when information really helps debugging the application!
- Multicore support when scheduling jobs with APScheduler
- Parent alerting (escalation)
- Core error alerting to [linspector]->members on internal errors
- Hostgroup parents (example: if the hostgroup "network" is down, don't alert for the hosts in that network)
- Add more tasks e.g. storage in mongodb or mariadb and some more notifications like XMPP and SMS
- Check for all required configuration options and set defaults in services.
- Write documentation and inline documentation.
- Add kwargs to notifications, tasks and maybe plugins.
- Add date and cron based scheduling to linspector.py to make the full use of APScheduler.
- Make Linspector Windows compatible (not so important)
