# Introduction

The following document provides detailed information on the components
that make up the architecture diagram below. 

<img src="./Architecture.png" width="650px">

## Keycloak / Single Sign on

Will use the existing keycloak service to provide the application with OIDC AuthN/Z
Information on keycloak integration:

* [SSO background information](https://bcgov.github.io/sso-requests)

Once we have a simple app created will request the SSO integration.

The diagram attempts to describe the authN/Z flow in a simplified way.  In 
a nutshell its a Proof of Key (PKCE) OIDC flow.  The frontend communicates with
keycloak eventually getting an access token in a Javascript Web Token format 
(JWT) which is consumed and verified by the frontend to Authenticate and Authorize
users, and it also uses this to authorize backend requests.


## Openshift

All the components that will be created to support the alerting app will 
be hosted on openshift.

Openshift namespaces have been provisioned.

## Frontend

Making the assumption that this will be some kind of typescript/javascript based
Single Page App (SPA) frontend, using one of the popular 

## Deployments

Ideally re-use the quickstart to create an application deployment

* [base quickstart repo for node/typescript/javascript apps](https://github.com/bcgov/quickstart-openshift)
* [if using java/go/python backend](https://github.com/bcgov/quickstart-openshift-backends)
