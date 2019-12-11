# Hashicorp Vault Plugin for XL Release

[![License: MIT][xlr-hashicorp-vault-plugin-license-image] ][xlr-hashicorp-vault-plugin-license-url]
[![Github All Releases][xlr-hashicorp-vault-plugin-downloads-image] ]()

[xlr-hashicorp-vault-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-hashicorp-vault-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-hashicorp-vault-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-hashicorp-vault-plugin/total.svg

# Overview

The [HashiCorp Vault](https://www.vaultproject.io/) plugin is an XL Release plugin that retrieves secrets from a Vault Server for use in your tasks and automations.  These secrets include static and dynamic username and password fields from the Secrets Engine of your choice.

## Requirements

* **XL Release requirements**
	* **XL Release**: version 9.5+
	
* **Plugin Testing requirements**
    * gradle
    * docker
    * a modern web browser
    * a linux-friendly CLI
    * XL CLI 9.5 or higher

## Installation

This plugin is presently built with gradle 6.0.1, as noted in `gradle/wrappter/gradle-wrapper.properties.`

Import the jar file into your `%XLRELEASE_INSTALLATION%/plugins/__local__` folder, or from the web UI as a new plugin.

## Usage

Define the server configuration of URL plus token.  These instructions TBD.


## Plugin build mechanics

### Testing with Docker
It is convenient to test your plugin against a local container.  The following command starts up the process:
`./gradlew runDockerCompose`

You may wish to follow the logs of the xlr container with the next command, as the default XLR container is named `xlr`:

`docker logs -t -f xlr`

The runDockerCompose assets are located in `src/test/resources/docker` primarily as the `docker-compose.yml` file.

###Build the software:
`./gradlew clean build`

###Set the version of Gradle:
`./gradlew wrapper --gradle-version=6.0.1 --distribution-type=bin`

###Check dependencies versions:
`./gradlew dependencyUpdate -Drevision=release`

###Release Software:
1. Create a pull request.  Make your changes, and tag your code with Major.Minor.Patch version numbers
1. Once the pull request is approved, our CI server builds up the software.  If it passes - 
1. The CI build publishes results to the GitHub Releases section.

## Testing

This repository includes "as-code" files to help you get started with a testing environment.

Start your build with runDockerCompose:

`./gradlew runDockerCompose`

Stop your test with stopDockerCompose:
`./gradlew stopDockerCompose`

These two URLs are defined by the contents in your src/test/resources/docker/docker-compose.yml file:

XLR: localhost:15516
Vault: localhost:15200

### Setting up Vault
Navigate to the Vault URL and configure your number of keys and how many are needed to unseal.  
We recommend 3 and 2, respectively.  Save your keys and master token for logging in later.
You may also configure the Vault sever from the CLI (that is an exercise for the reader).  
If you preserve your directory structure, your keys and token will persist on each runDockerCompose invocation.  

Once you setup Vault from the UI (or CLI), you can run these commands to setup your initial secrets engines.  The secrets engine creation is a one-time process for each persisted run.

```
vault login  s.ZT3LhH70qS2hOTjZ1w37TFxz # This value is specific to your instance
vault secrets enable -path=kv kv
vault secrets enable -version=2 -path=kv2 kv
vault secrets list
```

 
### Update src/test/resources/ascode/xebialabs/secrets.xvals 
Next, update your secrets to use the token in your XLR configuration.

* The vault token generated for your server (vault_Server_vault_test_token).  This default value will *not* work until you update the token for your system.
* The name of a secret value for your testing (vault_CreateSecret_Create_Secret_value).  The default is "test-password-123"
* The XLR admin user password for scripts (xlrelease_Release_vault_test_scriptUserPassword).  The default is "admin"

### Import the models

From your XL CLI, navigate to the `src/test/resources/ascode/` folder and run this command:

`xl apply --config blueprints.yaml -f xebialabs.yaml`

The file `blueprints.yaml` contains a blueprints definition for the local XLR server so you don't have to modify your current configuration.

