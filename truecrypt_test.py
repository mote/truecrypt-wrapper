
import unittest
import os

import truecrypt

test_file = '/home/mote/dev/truecrypt/test.dat'
test_pwd = 'test123'
test_mount = '/home/mote/dev/truecrypt/test_mount_pt'
test_clearfile = '/home/mote/dev/truecrypt/test_mount_pt/test_file'

# has one file inside, called "test_file", contents == 'success!'

class Tests(unittest.TestCase):
  def tearDown(self):
    truecrypt.dismount()
    os.rmdir(test_mount)

  def testCorrect(self):
    self.assertTrue(truecrypt.mount(test_file, test_pwd, test_mount))
    self.assertTrue(os.path.exists(test_clearfile))

  def testBadPassword(self):
    self.assertFalse(truecrypt.mount(test_file, 'bad_pass', test_mount))
    self.assertFalse(os.path.exists(test_clearfile))


if __name__ == "__main__":
  unittest.main()
