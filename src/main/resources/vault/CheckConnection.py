#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import hvac
from vault.Vault import Vault

logger.info("=== CHECK CONNECTION ==========================================")
client = hvac.Client(url=configuration.url,
                     token=configuration['token'])

if client.sys.is_initialized():
    logger.info(">> Vault is initialized")

    if client.sys.is_sealed():
        Vault.exit(Vault.VAULT_SERVER_SEALED, "Vault Server {} is Sealed".format(configuration.url))

    if configuration['token']:
        logger.info("Validating token configuration against {}".format(configuration['url']))

        if client.is_authenticated():
            logger.info(">> Your token request is for token is authenticated")
            logger.info("===============================================================")
        else:
            Vault.exit(Vault.VAULT_NOT_AUTHENTICATED, "Vault Server is not authenticated")

    else:
        Vault.exit(Vault.VAULT_NO_TOKEN, "You must use a token for Vault")
else:
    Vault.exit(Vault.VAULT_NOT_INITIALIZED, "Your Vault Server at {} is not initialized".format(configuration.url))
