# modstat

Python script for that generates CSV log of ADSL2+ modem status data. It is meant to be used with modems that are
based on tc3162 SoC (System on Chip), running Linux OS, such as mine D-Link DSL-2875AL. The data is extracted from
`/proc/tc3162/adsl_stats`. It is assumed that modem is running ssh server and the admin user password is known.
