# Hashicorp Vault Plugin for XL Release

[![License: MIT][xlr-hashicorp-vault-plugin-license-image]][xlr-hashicorp-vault-plugin-license-url]
[![Github All Releases][xlr-hashicorp-vault-plugin-downloads-image]]()
[![Build Status](https://travis-ci.org/xebialabs-community/xlr-hashicorp-vault-plugin.svg?branch=master)](https://travis-ci.org/xebialabs-community/xlr-hashicorp-vault-plugin)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/028a468d01c24cc192e167f776f0fe05)](https://www.codacy.com/manual/marcoman/xlr-hashicorp-vault-plugin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xebialabs-community/xlr-hashicorp-vault-plugin&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/9327483cb92b9a203d6d/maintainability)](https://codeclimate.com/github/xebialabs-community/xlr-hashicorp-vault-plugin/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/9327483cb92b9a203d6d/test_coverage)](https://codeclimate.com/github/xebialabs-community/xlr-hashicorp-vault-plugin/test_coverage)

## Overview

The [HashiCorp Vault](https://www.vaultproject.io/) plugin is an XL Release plugin
to retrieve  secrets from a Vault Server for use in your tasks and automations.
These secrets include static and dynamic username and password fields from the
Secrets Engine of your choice.

NOTE: This is presently a community plugin meant to prove the concept.  As such,
there are optimizations that should be made, which includes a reduction in the
liberal logging that *may* include secrets.

## Requirements

- XL Release: version 9.5+
- Plugin Testing requirements
  - Gradle
  - Docker
  - XL CLI 9.5 or higher

## Installation

This plugin is presently built with gradle 6.0.1, as noted in `gradle/wrappter/gradle-wrapper.properties.`

Import the jar file into your `%XLRELEASE_INSTALLATION%/plugins/__local__` folder,
or from the web UI as a new plugin.

## Usage

Define the server configuration of URL plus token.  These instructions TBD.

### Configuration

### Secrets Engine V1

### Secrets Engine V2

### Dynamic Secrets

### MySQL Secrets Engine

### AWS Secrets Engine

## Plugin build mechanics

### Testing with Docker

It is convenient to test your plugin against a local container.  The following command starts up the process:
`./gradlew runDockerCompose`

You may wish to follow the logs of the xlr container with the next command, as the default XLR container is named `xlr`:

`docker logs -t -f xlr`

The runDockerCompose assets are located in `src/test/resources/docker` primarily as the `docker-compose.yml` file.

## Testing with as-code

This repository includes "as-code" files to help you get started with a testing environment.

Start your build with runDockerCompose:

`./gradlew runDockerCompose`

Stop your test with stopDockerCompose:

`./gradlew stopDockerCompose`

These two URLs are defined by the contents in your src/test/resources/docker/docker-compose.yml file:

- XLR: [http://localhost:15516](http://localhost:15516)
- Vault: [http://localhost:15200](http://localhost:15200)

See the readme in the ascode folder for more details on the different models.

### Setting up Vault

Navigate to the Vault URL and configure your number of keys and how many are
needed to unseal.  We recommend 3 and 2, respectively.  Save your keys and
master token.  You may also configure the Vault sever from the CLI (that is
an exercise for the reader).  If you preserve your directory structure, your
keys and token values will persist on each runDockerCompose invocation, but
you will have to unseal the server.

Once you setup Vault from the UI (or CLI), you can run these commands to set up
your initial secrets engines.  The secrets engine creation is a one-time
process for each persisted run.

```shell script
vault login  s.ZT3LhH70qS2hOTjZ1w37TFxz # This value is specific to your instance
vault secrets enable -path=kv kv
vault secrets enable -version=2 -path=kv2 kv
vault secrets list
```

The commands above will configure secrets engines for the supplied XLR Template.

### Update src/test/resources/ascode/xebialabs/secrets.xvals

Next, update your secrets to use the token in your XLR configuration.

- The vault token generated for your server (vault_Server_vault_test_token).
  This default value will *not* work until you update the token for your system.
- The name of a secret value for your testing (vault_CreateSecret_Create_Secret_value).
  The default is "test-password-123"
- The XLR admin user password for scripts (xlrelease_Release_vault_test_scriptUserPassword).
  The default is "admin"

### Import the models

From your XL CLI, navigate to the `src/test/resources/ascode/` folder and run
this command:

`xl apply --config blueprints.yaml -f xebialabs.yaml`

The file `blueprints.yaml` contains a blueprints definition for the local XLR
server so you don't have to modify your current configuration.

The imported template are at the Vault folder as "vault-test."

[xlr-hashicorp-vault-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-hashicorp-vault-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-hashicorp-vault-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-hashicorp-vault-plugin/total.svg
