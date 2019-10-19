# modstat

Python script for that generates CSV log of ADSL2+ modem status data, sampled every 5 seconds. It is meant to be used with modems that are
based on tc3162 SoC (System on Chip), running Linux OS, such as mine D-Link DSL-2875AL.

The data is extracted from
`/proc/tc3162/adsl_stats`. It is assumed that modem is running ssh server and the admin user password is known. The script has it set
to `lozinka` as a default, so it needs to be adjusted.

Requires python 2.x and pexpect package to run. Invoke as

`python modstat.py`

or

`python -u modstat.py : tee log.csv`
