### Scaling Dash on AWS

Ths example utilizes AWS and Elastic Container Registry.  This example is mostly instructions to follow using the AWS MAnagement Console.  Automated implementation and deployment steps on other Cloud platforms can be added over time.

##### Creating a Docker container and pushing it to Amazon ECR

Perform the following steps to create a Docker image and container:

1.  download Docker on to your local system and execute Docker Desktop.
2.  Copy the `example.env` file to `.env`.
3.  Redefine the variables with your AWS account information and name of your app.
4.  Copy your app and associated source tree beneath src
5.  Execute `./docker_ecr.sh` to build your docker image and push it to an AWS Elastic Container Repositiory.
6.  NOTE: `./docker_ecr.sh` must be executed again whenever it does not complete with an `use of closed network connection` error

##### Creating an ECS cluster running the Dash container

Perform the following steps to create an Amazon ECS cluster running the Dash App.  If a particular setting isn't described here, assume the default is used.
Substitute **app** for the name of your app within each of the steps below:

1. Create two Security Groups 
   1. Traffic to the Load Balancer - port 80/443 - 0.0.0.0/0, Name: **app-alb-sg**
   2. Traffic from the Load Balancer – All TCP, Source=app-alb-sg, Name: **app-from-alb-sg**

2. Create an ECS Cluster
   1. Cluster Name: **app-cluster**
   2. Fargate Infrastructure (default) or selected EC2 Instances
   3. Create

3. Select Task Definition from the sidebar 
   1. Task Definition Family Name: **app-taskdef**
   2. Hardware Config: Select desired settings, 1CPU, 3GB usually works fine 
   3. Container Name: **app-container**
   4. Container Image URI: Container URI from ECR
   5. Create 
   
4. Create a Service 
   1. Select Clusters -> **app-cluster** -> Services -> Create 
      1. Deployment Configuration 
         1. Family: **app-taskdef**, RevisionL LATEST
         2. Service name: **app-service**
         3. Desired Tasks: select the number of hosted containers, 3 for example 
      2. Networking 
         1. Uncheck the default Security Group and select: **app-from-alb-sg**
      3. Load Balancing - Create a new Application Load Balancer, can select one created in advance 
         1. Type: Application Load Balancer 
         2. Name:  **app-alb**
         3. Port = 80, Protocol = HTTP 
         4. Target Group Name: **app-tg**
         5. Health Check Path: / 
         6. Grace Period: 30 
         7. **NOTE:** You cannot select the Load Balancer security group here and it gets incorrectly defined
      4. Create
         
5. EC2 -> Load Balancer -> **app-alb** -> Security -> Edit
   1. Uncheck **app-from-alb-sg** and select **app-alb-sg** -> Save Changes
   2. Copy the **DNS name** to test the connection
   
6. Verify Application 
   1. Check EC2 -> Target Groups -> **app-tg** systems are running as Healthy 
   2. Connect from a browser using http://**DNS Name**

##### Application Load Balancer Adjustments to allow Secure traffic

Perform the following modifications in order to connect to registered domain and utilize secure https traffic:

1. Within Route 53, Create a Hosted Zone for your registered domain
   1. Within the zones Hosted Zone Details, note the four DNS Name entries of the **NS** record
   2. Redefine the four DNS server entries on the Domains -> domain page to match the four defined within the Hosted Zone
   
2. From Route 53 -> Hosted Zones -> Hosted Zone connect Load Balancer to Hosted Zone 
   1. Delete any A records for previous attempts, if necessary
   2. Create Record 
   3. Click Alias 
   4. Select Zone, Application Load Balancer, and target ALB 
   5. Test your connection to the app using: http://appdomain.com
      
3. From Certificate Manager, request a Public Certificate for the domain
   1. Request a Public Certificate, Next
   2. Fully Qualified Domain Name: appdomain.com (no leading host string), Request 
   3. Click on Pending Validation Certificate 
   4. Click on Add CNAME record in Route 53 and wait for Status=Issued
   
4. From EC2 -> Load Balancers -> **app-alb** add https Listener to Load Balancer 
   1. Add Listener: HTTPS:443 
   2. Action: Forward to Target Group 
      1. Select Certificate 
      2. Add 
      3. Test with https://appdomain.com
      
5. From EC2 -> Load Balancers -> **app-alb** have Load Balancer redirect port 80 traffic to https port 443 
   1. Select HTTP:80 
   2. Select Manage Rules -> Edit Rule 
   3. Select Actions -> Delete Listener
   4. Select Actions -> Add Listener
      1. HTTP: 80
      2. Redirect to URL
      3. HTTPS: 443
      4. Add 
   5. Wait a minute and test with http://appdomain.com redirecting to https://appdomain.com

The initial Public Certificate works for domain.com and www.appdomain.com.
To support https traffic to any other host.appdomain.com address, an additional Public Certificate must be created for 
each target host or create a *.appdomain.com cerficate which is not recommended.

##### Cluster Deletion Steps

1. Cluster -> **app-service** -> delete service
2. Cluster -> Task Definition -> revision -> Actions -> Deregister, then Delete
3. Cluster -> **app-cluster** -> delete cluster
4. EC2 -> Load Balancers -> **app-alb** -> Delete
5. EC2 -> Target Groups -> **app-tg** -> Delete
6. (if necessary) ECR -> **app-repository** -> Delete