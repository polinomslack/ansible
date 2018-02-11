#!/usr/bin/env python
import subprocess,smtplib,socket,time
import logging,logging.handlers
from email.mime.text import MIMEText
import os.path

lockfileError = "/tmp/iptablesAlertErr.lck"
lockfileEmpty = "/tmp/iptablesAlertEmpt.lck"

def sendmail(message):
  sender="iptables@"+socket.gethostname()
  recepient='admin@myhost.com'
  msg = MIMEText(message)
  msg['Subject'] = "IPTables alert at "+socket.gethostname()
  msg['From'] = sender
  msg['To'] = recepient
  server = smtplib.SMTP('myhost.com',25)
  server.sendmail(sender,recepient,msg.as_string())

#get the number of currenly loaded rules and stdout of command which loads a ruleset
def getFwLineNum():
  fwCmd = subprocess.Popen(['/sbin/iptables', '-S'], stdout=subprocess.PIPE)
  fwCmdOutput = fwCmd.stdout.read()
  return  len(fwCmdOutput.splitlines())

applyRulesCmd = 0

#Initiate logging
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.SysLogHandler(address = '/dev/log')
my_logger.addHandler(handler)

if getFwLineNum() < 15:
  #we should create lock file here, which will warn about empty rules
  restoreTestCmd = subprocess.Popen(['/sbin/iptables-restore','-t','-v','/etc/iptables/rules.v4'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  resultOfTestCmd = restoreTestCmd.communicate()
  if restoreTestCmd.returncode == 0:
    applyRulesCmd = subprocess.call(['/sbin/iptables-restore','/etc/iptables/rules.v4'])
    try:
      os.remove(lockfileError)
    except:
      pass
    #we should recheck amount of lines here, if it is fine just remove lock
    #if it is not fine, script must send a message with emtpy ruleset warning
    time.sleep(5)
    if getFwLineNum() < 15:
      if not os.path.exists(lockfileEmpty):
        message = 'Ruleset file is empty by some reason!'
        my_logger.critical('iptables-cron.py: Ruleset file is empty by some reason!\n' + message)
        sendmail(message)
        try:
          open(lockfileEmpty, 'a').close()
        except:
          pass
    else:
      try:
        os.remove(lockfileEmpty)
      except:
        pass
  else:
    if not os.path.exists(lockfileError):
      message= 'Rules could not be loaded with next message:\n' + resultOfTestCmd[1]
      my_logger.critical('iptables-cron.py: syntax error occured\n'+message)
      sendmail(message)
      try:
        open(lockfileError,'a').close()
      except:
        pass
    applyRulesCmd = 1
else:
  if os.path.exists(lockfileEmpty):
    try:
      os.remove(lockfileEmpty)
    except:
      pass
  if os.path.exists(lockfileError):
    try:
      os.remove(lockfileError)
    except:
      pass
exit(applyRulesCmd)