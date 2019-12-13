#
# Copyright 2019 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import logging

from vault import VaultClient

logger = logging.getLogger("Vault")
logger.info("VAULT: Executing %s" % task.getTaskType())
print("VAULT: Executing %s" % task.getTaskType())
vault_client = VaultClient(vaultServer, token=vaultServer['token'], logger=logger)

# Use the name of the type in multiple places.
mytype = str(task.getTaskType())
logger.info("=== VAULT SECRET V2 : {} ===".format(mytype))

if not vault_client.client.sys.is_initialized():
    vault_client.exit(vault_client.VAULT_NOT_INITIALIZED,
                      "Your Vault Server at {} is not initialized".format(vaultServer['url']))

if vault_client.client.sys.is_sealed():
    vault_client.exit(vault_client.VAULT_SERVER_SEALED, "Vault Server {} is Sealed".format(vaultServer['url']))

if vaultServer['token'] is None:
    vault_client.exit(vault_client.VAULT_NO_TOKEN, "You must use a token for Vault")

if not vault_client.client.is_authenticated():
    vault_client.exit(vault_client.VAULT_NOT_AUTHENTICATED, "Vault Server is not authenticated")

# vault.SecretsV2.Read
if mytype == 'vault.SecretsV2-Configure':
    response = vault_client.client.secrets.kv.v2.configure(
        max_versions=max_versions,
        mount_point=mount_point,
        cas_required=cas_required
    )
    logger.info("SecretsV2-Configuration response is {}".format(response))

elif mytype == 'vault.SecretsV2-EnableEngine':
    logger.info("SecretsV2-EnableEngine Not Implemented")

elif mytype == 'vault.SecretsV2-ReadConfiguration':
    kv_configuration = vault_client.client.secrets.kv.v2.read_configuration(mount_point=mount_point)
    logger.info('Config under path "kv": max_versions set to "{max_ver}"'.format(
        max_ver=kv_configuration['data']['max_versions'],))
    logger.info('Config under path "kv": check-and-set require flag set to {cas}'.format(
        cas=kv_configuration['data']['cas_required'],))

elif mytype == "vault.SecretsV2-ReadSecretVersions":
    secret_version_response = vault_client.client.secrets.kv.v2.read_secret_version(
        path=path,
        version=version,
        mount_point=mount_point
    )
    logger.info('Version {} of secret under path {} contains the following keys: {data}'.format(
        version, path, data=secret_version_response['data']['data'].keys(),))
    logger.info('Version {} of secret under path {} created at: {date}'.format(
        version, path, date=secret_version_response['data']['metadata']['created_time'],))

elif mytype == "vault.SecretsV2-CreateSecret":
    logger.info('CreateSecret has these values for path, key, cas = {},{},{}'.format(path, key, cas))
    print('CreateSecret has these values for path, key, cas = {},{},{}'.format(path, key, cas))
    newsecret = {key : value}
    if cas:
        response = vault_client.client.secrets.kv.v2.create_or_update_secret(
            path=path,
            secret=newsecret,
            cas=cas,
            mount_point=mount_point
        ) # Raises hvac.exceptions.InvalidRequest
    else:
        response = vault_client.client.secrets.kv.v2.create_or_update_secret(
            path=path,
            secret=newsecret,
            mount_point=mount_point
        )
    version = response['data']['version']
    print("VAULT: Response = %s" % response)

elif mytype == "vault.SecretsV2-PatchExistingSecret":
    response = vault_client.client.secrets.kv.v2.patch(
        path=path,
        secret=dict(key=value),
        mount_point=mount_point
    )

elif mytype == "vault.SecretsV2-DeleteVersion":
    if latest: # Delete the latest version
        response = vault_client.client.secrets.kv.v2.delete_latest_version_of_secret(
            path=path,
            mount_point=mount_point
        )
    else: # Need to delete a specific version
        response = vault_client.client.secrets.kv.v2.delete_latest_version_of_secret(
            path=path,
            mount_point=mount_point,
            versions=version
        )

elif mytype == "vault.SecretsV2-UndeleteVersion":
    response = vault_client.client.secrets.kv.v2.undelete_secret_versions(
        path=path,
        mount_point=mount_point,
        versions=versions,
    )
    logger.info("Response is {}".format(response))

elif mytype == "vault.SecretsV2-DestroyVersion":
    response = vault_client.client.secrets.kv.v2.destroy_secret_versions(
        path=path,
        mount_point=mount_point,
        versions=versions,
    )
    logger.info("Response is {}".format(response))

elif mytype == "vault.SecretsV2-ListSecrets":
    response = vault_client.client.secrets.kv.v2.list_secrets(
        path=path,
        mount_point=mount_point
    )

    logger.info('The following paths are available under {} prefix: {keys}'.format(
        path,
        keys=','.join(list_response['data']['keys']),
    ))
    logger.info("Response is {}".format(response))

elif mytype == "vault.SecretsV2-ReadSecretMetadata":
    hvac_path_metadata = vault_client.client.secrets.kv.v2.read_secret_metadata(
        path=path,
        mount_point=mount_point
    )
    logger.info('Metadata under path {} is {}'.format(
        path, hvac_path_metadata))

elif mytype == "vault.SecretsV2-UpdateMetaData":

    response = vault_client.client.secrets.kv.v2.update_metadata(
        path=path,
        mount_point=mount_point,
        max_versions=max_versions,
        cas_required=cas
    )
    logger.info("Response is {}".format(response))

elif mytype == "vault.SecretsV2-DeleteMetaDataAndAllVersions":
    response = vault_client.client.secrets.kv.v2.delete_metadata_and_all_versions(
        path=path,
    )
    logger.info("Response is {}".format(response))

else:
    logger.info("Not Implemented {}".format(mytype))

