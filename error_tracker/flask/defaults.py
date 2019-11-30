# -*- coding: utf-8 -*-
#
#    Error tracker flasks plugins default value
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#

# Whether notification should be send or not
APP_ERROR_SEND_NOTIFICATION = False
# List of email recipients, these users would be send an email
APP_ERROR_RECIPIENT_EMAIL = None
# Error email subject prefix
APP_ERROR_SUBJECT_PREFIX = ""
# Sensitive data masking value
APP_ERROR_MASK_WITH = "**************"
# what all sensitive data should be masked, this means any variables whose name have
# either password or secret would be masked
APP_ERROR_MASKED_KEY_HAS = ("password", "secret")
# APP URL prefix where endpoint would be exposed
APP_ERROR_URL_PREFIX = "/dev/error"
# Email sender user email's ID
APP_ERROR_EMAIL_SENDER = None
# In Exceptions listing page, number of entry should be displayed
APP_DEFAULT_LIST_SIZE = 20
