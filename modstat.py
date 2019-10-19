from __future__ import print_function
import os
import tempfile
import pexpect
import time

def do_ssh(host, cmd, user, password, timeout=30, bg_run=False):
    """SSH'es to a host using the supplied credentials and executes a command.
    Throws an exception if the command doesn't return 0.
    bgrun: run command in the background"""

    fname = tempfile.mktemp()
    fout = open(fname, 'w')

    options =  ' -q -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null'
    options += ' -oPubkeyAuthentication=no'
    options += ' -oKexAlgorithms=+diffie-hellman-group1-sha1'

    if bg_run:
        options += ' -f'
    ssh_cmd = 'ssh %s@%s %s "%s"' % (user, host, options, cmd)
    child = pexpect.spawn(ssh_cmd, timeout=timeout)
    child.expect(['password: '])
    child.sendline(password)
    child.logfile = fout
    child.expect(pexpect.EOF)
    child.close()
    fout.close()

    fin = open(fname, 'r')
    stdout = fin.read()
    fin.close()
    os.remove(fname)

    if 0 != child.exitstatus:
        raise Exception(stdout)

    return stdout

def find_v(lines, name):
    for s in lines:
        pair = s.split(':')
        if len (pair) == 1:
            continue
        else:
            if pair[0] == name:
                return pair[1].strip()
    return ''

vnames = ['ADSL link status',
          'near-end interleaved channel bit rate',
          'far-end interleaved channel bit rate',
          'noise margin downstream',
          'near-end FEC error interleaved',
          'near-end CRC error interleaved',
]

modem = '192.168.1.1'
user  = 'admin'
pswd  = 'lozinka'
cmd   = 'cat /proc/tc3162/adsl_stats'

print('time,status,down rate,up rate,down SNR mrg,FEC,CRC')
while 1:
    stats  = do_ssh(modem, cmd, user, pswd)
    lstat = stats.splitlines()

    localtime = time.localtime(time.time())
    p =time.strftime("%d/%m %H:%M:%S,", localtime)
    for n in vnames:
        p += find_v(lstat, n)
        p += ','
    p = p[:-1]
    print(p)
    time.sleep(5)
