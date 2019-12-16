# As-code Template help

This folder contains different assets to help you verify and test the plugin.
This template was tested against XLR 9.0.6 and XL CLI 9.5.0

## Configure Vault

Make sure you navigate to [http://localhost:15200](http://localhost:15200)
and unseal  your vault.

These next commands will ensure you have the right secrets engines setup.
For now, let's assume people that use this plugin will NOT be creating secrets
engines from XLR.  Of course, this could change.

```shell script
export VAULT_ADDR='http://127.0.0.1:15200'
export VAULT_DEV_ROOT_TOKEN_ID="s.o4fcEz1aqAHcZuKDeE6TGjg0"
ult login s.o4fcEz1aqAHcZuKDeE6TGjg0
vault secrets enable -path=kv kv
vault secrets enable -version=2 -path=kv2 kv
vault secrets list
```

Your ROOT token ID will be different, and best practices are to use something
other than the ROOT token in production.

## Configure XLR

In this directory, we include a configuration file to point to the assumed
local XLR server.  This command will load up the template:

```shell script
xl apply --config blueprints.yaml -f xebialabs.yaml
```

In XLR, this template creates a Vault/vault-test Template.  When you run this
template, you are guided through the different steps to create and update
secrets.  In the present form, these secret engines are supported:

- Secrets Engine V1
- Secrets Engine V2.  This includes outputs to show the version of the secret.

The template approximates some real-world scenarios *as well as some contrived
use cases.*  You are urged to evaluate the applicability fo the example for
your use case.

The next steps are to include secrets engine support for:

- AWS
- Dynamnic
- MySQL
- Others as demanded and time permits.


