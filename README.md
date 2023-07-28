# scalingDash

This project defines steps to implement a scalable and secure Plotly Dash Open Source deployment for cases when supporting hundreds, if not thousands of connections is necessary.
While created for Plotly Dash, these intructions are likely to work for any containerized application.

The three steps required to achieve this goal are:

1. Create a docker container for the app and upload it to a Container Registry
2. Launch the container within a Cluster framework
3. Have the Cluster accept http and https traffic from your registered domain

The example manages scaling of the Dash web app only.  Each instance must connect to a remote database or other data source, if neceesary.

While these instructions work for any Plotly Dash app, a simple one is included

### Scaling Dash on AWS

The first example uses AWS and Elastic Container Registry.  Implementation on other Cloud environments can be added over time.

##### Creating the Docker container and pushing to Amazon ECR

To create a Docker image and container, download Docker on to your local system and execute Docker Desktop.

AWS Account Information must be defined in a manner similar to the example below:

```
export AWS_ACCESS_KEY_ID=AKIAQ3BABJM6G2LGWXYV  
export AWS_SECRET_ACCESS_KEY=Z+lB9erJBEncKO4z0asrIQ1eImYp4Cm5s89G9WgB   
export AWS_REGION=us-west-2   
export AWS_ACCOUNT_ID=058273491184    
export APP_NAME=dashmath    
export APP_VERSION=1.0   
```

AWS Account Information can be registered on the system using the following commands:

```
aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
aws configure set region $AWS_REGION
```

The following commands can be executed to create a Docker container image and push it to the Elastic Container Registry:

```
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
aws ecr create-repository --repository-name $APP_NAME-repository
docker build -t $APP_NAME .

# notice version setting as TAG of #docker images
docker tag $APP_NAME:$APP_VERSION $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$APP_NAME-repository
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$APP_NAME-repository
```

##### Creating an ECS cluster running the Dash container

Perform the following steps to create an Amazon ECS cluster running the Dash App.  If a particular setting isn't described here, assume the default is used.
Substitute **app** for the name of your app within each of the steps below:

1. Create two Security Groups 
   1. Traffic to the Load Balancer - port 80/443 - 0.0.0.0/0, Name: **app-alb-sg**
   2. Traffic from the Load Balancer – All TCP, Source=app-alb-sg, Name: **app-from-alb-sg**

2. Create an ECS Cluster
   1. Cluster Name: **app-cluster**
   2. Fargate Infrastructure
   3. Create

3. Select Task Definition from the sidebar 
   1. Task Definition Family Name: **app-taskdef**
   2. Hardware Config: Select desired settings, 1CPU, 3GB usually works fine 
   3. Container Name: **app-container**
   4. Container Image URI: Container URI from ECR
   5. Next, Create 
   
4. Create a Service 
   1. Select Clusters -> **app-cluster** -> Services -> Create 
      1. Deployment Configuration 
         1. Family: **app-taskdef**
         2. Service name: **app-service**
         3. Tasks: select the number of hosted containers 
      2. Networking 
         1. Security Group: **app-from-alb-sg**
      3. Load Balancing - Create a new Application Load Balancer, can select one created in advance 
         1. Type: Application Load Balancer 
         2. Name:  **app-alb**
         3. Port = 80, Protocol = HTTP 
         4. Target Group Name: **app-tg**
         5. Health Check Path: / 
         6. Grace Period: 30 
         7. **NOTE:** You cannot select the Load Balancer security group here and it gets incorrectly defined
         
4. EC2 -> Load Balancer -> **app-alb**
   1. Correct Security Group: **app-alb-sg**
   2. Copy the **DNS name** to test the connection
   
5. Verify Application 
   1. Check Target Group **app-tg** systems are running as Healthy 
   2. Connect from a browser using http://**DNS Name**

##### Application Load Balancer Adjustments

Perform the following modifications in order to connect to registered domain and utilize secure https traffic:

1. Within Route 53, Create a Hosted Zone for your registered domain
   1. Within the zones Hosted Zone Details, note the four DNS Name entries of the **NS** record
   2. Redefine the four DNS server entries on the Domains -> domain page to match the four defined within the Hosted Zone
   
2. From EC2 -> Load Balancer -> **app-alb**, establish a secure connection to your domain 
   1. Connect Load Balancer to Hosted Zone 
      1. Create Record 
      2. Click Alias 
      3. Select Zone, Application Load Balancer, and target ALB 
      4. Test your connection to the app using: http://appdomain.com
      
3. From Certificate Manager, request a Public Certificate for the domain
   1. Request a Public Certificate, Next
   2. Fully Qualified Domain Name: appdomain.com (no leading host string), Request 
   3. Click on Pending Validation Certificate 
   4. Click on Add CNAME record in Route 53 and wait for Status=Issued
   
4. Add https Listener to Load Balancer 
   1. Add Listener: HTTPS:443 
   2. Action: Forward to Target Group 
      1. Select Certificate 
      2. Add 
      3. Test with https://appdomain.com
      
5. Have Load Balancer redirect port 80 traffic to https port 443 
   1. Select Port 80 
   2. Edit 
   3. Remove
   4. Add Action -> Redirect 
   5. HTTPS: 443 
   6. Wait a minute and test with http://appdomain.com redirecting to https://appdomain.com
   
6. Allow traffic to www.appdomain.com
   1. From Route 53 -> Hosted Zone -> appdomain.com, click Create Record
   2. Record Name: www.appdomain.com
   3. Click Alias
   4. Route traffic to: Application and Classic Load Balancer
   5. Region: Cluster Region
   6. Choose Load Balancer: **app-alb**
   7. Create Records

The initial Public Certificate works for domain.com and www.appdomain.com.
To support https traffic to any other host.appdomain.com address, an additional Public Certificate must be created for 
each target host or create a *.appdomain.com cerficate which is not recommended.
