import os
import subprocess
import sys

def _run(cmd):
  return subprocess.Popen(cmd, shell=True,
      stdout=subprocess.PIPE, close_fds=True).stdout.read().rstrip()

CMD = '/usr/bin/truecrypt --text --non-interactive '

def mount(volume, password, mount_point):
  """Mount volume at location. Return True upon success."""
  if not os.path.exists(mount_point):
    os.mkdir(mount_point)
  cmd = '%s -p "%s" %s %s 2>&1' % (CMD, password, volume, mount_point)
  result = _run(cmd)
  if result:
    #sys.stderr.write('Problem: %s\n'% result)
    return False
  return True

def dismount():
  result = _run(CMD + '-d')


