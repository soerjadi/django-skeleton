# -*- coding: utf-8 -*-

"""
@author: Suryadi Sulaksono
"""

from django.core.mail import EmailMessage
from django.conf import settings
from apps.utils.asynchronous import asynchronous

import logging


class Mailer:
    """
    This class is for send mail
    """
    def __init__(self, subject, content, content_type, recipient_list, header=None, attachment=None):
        self.subject = subject
        self.content = content
        self.recipient_list = recipient_list
        self.header = header
        self.content_type = content_type
        self.attachment = attachment
        self.logger = logging.getLogger('django')

    @asynchronous
    def send(self):
        """
        This method will bring you to asynchronous mode and will give you alert when
        get an error to log file
        """
        try:
            msg = EmailMessage(self.subject, self.content, settings.EMAIL_HOST_USER, self.recipient_list,
                               headers=self.header)

            if self.content_type == "html":
                msg.content_subtype = "html"

            if self.attachment:
                msg.attach_file(self.attachment)

            print("sending email to %s from %s" % (self.recipient_list, settings.EMAIL_HOST_USER))

            return msg.send()
        except Exception as e:
            self.logger.error(e)
            pass

    def send_blocking(self):
        """
        This method will send email on blocking mode and will give you alert when
        get an error to log file
        """
        try:
            msg = EmailMessage(self.subject, self.content, settings.EMAIL_HOST_USER, self.recipient_list,
                               headers=self.header)

            if self.content_type == "html":
                msg.content_subtype = "html"

            if self.attachment:
                msg.attach_file(self.attachment)

            print("sending email to %s from %s" % (self.recipient_list, settings.EMAIL_HOST_USER))

            return msg.send()
        except Exception as e:
            self.logger.error(e)
            pass
