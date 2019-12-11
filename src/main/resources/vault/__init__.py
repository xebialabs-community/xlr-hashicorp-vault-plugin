#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
import sys
import hvac
from org.slf4j import Logger
from org.slf4j import LoggerFactory

class VaultClient(object):
    # TODO: Consider adding support for headers
    # TODO: Consider adding support for namespace
    # TODO: Consider adding support for TTL
    # TODO: May need to consider adding/handling redirects (allow_redirects)

    # It is convenient to have separate values for exit codes, instead of the usual exit(1)
    VAULT_SERVER_SEALED = 1
    VAULT_NOT_AUTHENTICATED = 2
    VAULT_NO_TOKEN = 3
    VAULT_NO_SERVER_PROVIDED = 4
    VAULT_NOT_INITIALIZED = 5

    def __init__(self, configuration, token, logger=None):
        self.logger = logger
        self.logger.info("=== VAULT START INITIALIZE ===")
        self.host = configuration['url']
        self.token = token

        if self.host is None:
            self.exit(self.VAULT_NO_SERVER_PROVIDED, "No Server was provided")
        if self.token is not None:
            self.client = hvac.Client(self.host, token)
        else:
            self.exit(self.VAULT_NO_TOKEN, "No Token provided")
        self.logger.info("=== VAULT END INITIALIZE ===")

    @staticmethod
    def exit (code, message):
        self.logger.error("VAULT ({}) {}".format(code, message))
        exit("VAULT ({}) {}".format(code, message))
    #        exit(code)

    # TODO: I am not sure we need this.  The operation is simple and we can inline the conditional elsewhere.
    def get_init(self):
        if (self.client.sys.is_initialized()):
            self.logger.info('Vault is initialized at %', url)
            return data
        else:
            Vault.exit(Vault.VAULT_NOT_INITIALIZED, "Vault is not initialized at {}".format(url))
