# author: WatchDogOblivion
# description: TODO
# WatchDogs SMTP Arguments

from watchdogs.base.models import Args
from watchdogs.utils.Constants import (EMPTY)


class SMTPArgs(Args):  # pylint: disable=too-many-instance-attributes

  VERSION = "SMTP args version: 1.0"

  def __init__(  # pylint: disable=too-many-arguments
      self, remoteHost="10.11.1.229", remotePort=25, name=EMPTY, password=EMPTY, senderEmail=EMPTY,
      recipientEmails=None, subject="Testing", body="This is a test", bodyType="html", mimeVersion="1.0",
      attachments=None):
    #type: (str, int, str, str, str, str, str, str, str, str, list) -> None
    super(SMTPArgs, self).__init__()
    self.remoteHost = remoteHost
    self.remotePort = remotePort
    self.name = name
    self.password = password
    self.senderEmail = senderEmail
    self.recipientEmails = recipientEmails
    self.subject = subject
    self.body = body
    self.bodyType = bodyType
    self.mimeVersion = mimeVersion
    self.attachments = attachments

  def getVersion(self):  #type: () -> str
    return SMTPArgs.VERSION

  def addArguments(self):  #type: () -> SMTPArgs
    RH_HELP = "Specify the remote host."
    RP_HELP = "Specify the SMTP port. The default is 25"
    N_HELP = "Specify the name of the user to login with"
    P_HELP = "Specify the password of the user to login with"
    SE_HELP = "Specify the email address of the sender."
    RE_HELP = "Specify the email address of recipient"
    S_HELP = "Specify the email subject."
    B_HELP = "Specify the email body."
    BT_HELP = "Specify the email body content type. The default is 'html' instead of 'plain'."
    MV_HELP = "Specify the MIME version"
    A_HELP = "Specify the email attachments"

    parser = self.getParser()
    required = parser.add_argument_group("Required SMTP arguments")
    required.add_argument("-rh", "--remote-host", required=True, help=RH_HELP, type=str,
                          metavar="10.11.1.229")
    required.add_argument("-n", "--name", required=True, help=N_HELP, type=str, metavar=EMPTY)
    required.add_argument("-p", "--password", required=True, help=P_HELP, type=str, metavar=EMPTY)
    required.add_argument("-re", "--recipient-emails", required=True, help=RE_HELP, nargs='+', type=str,
                          metavar=EMPTY)

    optional = parser.add_argument_group("Optional SMTP arguments")
    optional.add_argument("-rp", "--remote-port", help=RP_HELP, type=int, metavar=EMPTY, default=25)
    required.add_argument("-se", "--sender-email", help=SE_HELP, type=str, metavar=EMPTY,
                          default="eric@thinc.local")
    optional.add_argument("-s", "--subject", help=S_HELP, type=str, metavar=EMPTY, default="Testing")
    optional.add_argument("-b", "--body", help=B_HELP, type=str, metavar=EMPTY, default="This is a test")
    optional.add_argument("-bt", "--body-type", help=BT_HELP, type=str, metavar=EMPTY, default="html")
    optional.add_argument("-mv", "--mime-version", help=MV_HELP, type=str, metavar=EMPTY, default="1.0")
    optional.add_argument("-a", "--attachments", help=A_HELP, nargs='+', type=str, metavar=EMPTY)

    return self
