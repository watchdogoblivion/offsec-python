# author: WatchDogOblivion
# description: TODO
# WatchDogs SMTP Service

import os
import smtplib
import mimetypes

from email import encoders
from email import message  # pylint: disable=unused-import
from email.header import Header
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart  # pylint: disable=unused-import

from watchdogs.base.models import AllArgs, Common  # pylint: disable=unused-import
from watchdogs.mail.parsers import SMTPArgs
from watchdogs.utils.Constants import (COMMA, RB, FS, APPLICATION_OCTET_STREAM, CONTENT_DISPOSITION, ASCII,
                                       FROM, TO, SUBJECT, MIME_VERSION, ATTACHMENT)


class SMTPService(Common):

  @staticmethod
  def getMimeAttachment(filepath):
    #type: (str) -> MIMENonMultipart | message.Message
    if not os.path.isfile(filepath):
      return None
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
      ctype = APPLICATION_OCTET_STREAM
    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':
      openedFile = open(filepath)
      mimeAttachment = MIMEText(openedFile.read(), _subtype=subtype)
      openedFile.close()
    elif maintype == 'image':
      openedFile = open(filepath, RB)
      mimeAttachment = MIMEImage(openedFile.read(), _subtype=subtype)
      openedFile.close()
    elif maintype == 'audio':
      openedFile = open(filepath, RB)
      mimeAttachment = MIMEAudio(openedFile.read(), _subtype=subtype)
      openedFile.close()
    else:
      openedFile = open(filepath, RB)
      mimeAttachment = MIMEBase(maintype, subtype)
      mimeAttachment.set_payload(openedFile.read())
      openedFile.close()
      encoders.encode_base64(mimeAttachment)
    mimeAttachment.add_header(CONTENT_DISPOSITION, ATTACHMENT, filename=filepath.split(FS)[-1])
    return mimeAttachment

  @staticmethod
  def getMimeMessage(allArgs):
    #type: (AllArgs) -> MIMEMultipart
    sMTPArgs = allArgs.getArgs(SMTPArgs)

    attachments = sMTPArgs.attachments
    if (attachments):
      mimeMessage = MIMEMultipart()
      mimeMessage.attach(MIMEText(sMTPArgs.body, sMTPArgs.bodyType))
      for filepath in attachments:
        mimeMessage.attach(SMTPService.getMimeAttachment(filepath))
    else:
      mimeMessage = MIMEText(sMTPArgs.body, sMTPArgs.bodyType)
      mimeMessage[MIME_VERSION] = Header(sMTPArgs.mimeVersion, ASCII)

    mimeMessage[FROM] = Header(sMTPArgs.senderEmail, ASCII)
    mimeMessage[TO] = Header(COMMA.join(sMTPArgs.recipientEmails), ASCII)
    mimeMessage[SUBJECT] = Header(sMTPArgs.subject, ASCII)
    mimeMessage.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    return mimeMessage

  @staticmethod
  def sendEmail(allArgs):
    #type: (AllArgs) -> None
    sMTPArgs = allArgs.getArgs(SMTPArgs)
    try:
      sMTP = smtplib.SMTP(sMTPArgs.remoteHost, sMTPArgs.remotePort)
      sMTP.set_debuglevel(1)
      sMTP.login(sMTPArgs.name, sMTPArgs.password)
      mimeMessage = SMTPService.getMimeMessage(allArgs).as_string()
      sMTP.sendmail(sMTPArgs.senderEmail, sMTPArgs.recipientEmails, mimeMessage)
      sMTP.close()
      print("Successfully sent email")
    except smtplib.SMTPException:
      print("Error: unable to send email")
