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

import logging

from vault import VaultClient

logger = logging.getLogger("Vault")
logger.info("VAULT: Executing %s" % task.getTaskType())
print("VAULT: Executing %s" % task.getTaskType())
vault_client = VaultClient(vaultServer, token=vaultServer['token'], logger=logger)

# Use the name of the type in multiple places.
mytype = str(task.getTaskType())
logger.info("=== VAULT SECRET V1 : {} ===".format(mytype))
print("=== VAULT SECRET V1 : {} ===".format(mytype))

if vault_client.client.sys.is_initialized():
    logger.info("Vault Initialized:{}".format(vaultServer['url']))
else:
    vault_client.exit(vault_client.VAULT_NOT_INITIALIZED,
                      "Your Vault Server at {} is not initialized".format(vaultServer['url']))

if vault_client.client.sys.is_sealed():
    vault_client.exit(vault_client.VAULT_SERVER_SEALED, "Vault Server {} is Sealed".format(vaultServer['url']))

if vaultServer['token']:
    logger.info("Using Vault Token")
else:
    vault_client.exit(vault_client.VAULT_NO_TOKEN, "You must use a token for Vault")

if vault_client.client.is_authenticated():
    logger.info("Vault authenticated against {}".format(vaultServer['url']))
else:
    vault_client.exit(vault_client.VAULT_NOT_AUTHENTICATED, "Vault Server is not authenticated")

if mytype == 'vault.SecretsV1-ReadSecret':
    key_path = path + '/' + key
    logger.info("Reading from {}".format(key_path))
    print("Reading from {}".format(key_path))
    read_response = vault_client.client.secrets.kv.v1.read_secret(mount_point=mount_point, path=path)
    logger.info(">> Read Request complete for {}/{}/{} - {}".format(mount_point, path, key, read_response))
    print(">> Read Request complete for {}/{}/{} - {}".format(mount_point, path, key, read_response))
    value = read_response['data'][key]
    logger.info("===============================================================")
    print("===============================================================")

elif mytype == 'vault.SecretsV1-ReadDynamicSecret':
    logger.info("ReadDynamic Not Implemented")

elif mytype == 'vault.SecretsV1-CreateSecret':
    new_secret = {key: value}
    # TODO: Delete the next line once we know this write operation works.
    logger.info(">> Writing {} to {}".format(new_secret, path))
    print(">> Writing {} to {}".format(new_secret, path))
    create_response = vault_client.client.secrets.kv.v1.create_or_update_secret(mount_point=mount_point,
                                                                                path=path,
                                                                                secret=new_secret)
    logger.info(">> Write Request complete for {} : {}".format(path, create_response))
    logger.info("===============================================================")
    print(">> Write Request complete for {} : {}".format(path, create_response))
    print("===============================================================")

elif mytype == 'vault.SecretsV1-DeleteSecret':
    delete_response = vault_client.client.secrets.kv.v1.delete_secret(
        mount_point=mount_point,
        path=path,
    )
    logger.info(">> Delete Request complete for {}/{} - {}".format(mount_point, path, delete_response))
    logger.info("===============================================================")

elif mytype == 'vault.SecretsV1-EnableEngine':
    logger.info("Enable Engine Not Implemented")

else:
    logger.info("Not Implemented {}".format(mytype))

