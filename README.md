# scalingDash

This project defines steps to implement a scalable and secure Plotly Dash Open Source deployment.  
Such steps are neccessary to build a public facing application capable of handling hundreds, if not thousands of simultaneous connections.      

These steps were created for a Plotly Dash deployment, but they are also likely to work to properly scale and secure any containerized application.  The example manages scaling of the Dash web app only.  Each instance must connect to a remote database or other data source, if neceesary.  These instructions work for any Plotly Dash app and a simple one is included to use as an example.

Three steps are necessary to achieve this goal:

1. Creating a docker container for the app and upload it to a Container Registry
2. Launching one or more instaces running the container within a Cluster
3. Configuring the Cluster to accept http and https traffic from your registered domain

Deployment instructions for each Cloud Platform are listed in the following directories:

* AWS

Deployment can be performed in two ways:

* Manually using each provider's Management Console
* Automatically defined using aws cli commands
