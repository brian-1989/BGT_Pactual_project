# BGT PACTUAL Project

## **Description**
The BGT Pactual project is a web application developed in FastAPI. It allows the user to subscribe to the funds offered by the bank, and each fund has a minimum subscription amount. When the user subscribes, a notification can be sent via Email or SMS. The funds offered are as follows: the Voluntary Pension Fund (FPV) and Collective Investment Funds (FICs). It also allows the user to opt out or unsubscribe from a fund, and when this happens, the client is refunded the subscription amount. The platform provides the user with the ability to view all their fund transactions (Openings and Cancellations).


## **Table of Contents**
1. [Installation](#installation)
2. [Use](#use)
3. [Endpoints](#endpoints)
4. [Autor](#autor)

## **Installation**

### **Prerequisites**
- Docker
- Docker Compose
- Docker Desktop
- Git

### **Install docker**
If you don't have Docker, Docker Compose, and Docker Desktop installed on your machine, I suggest these links to do so.
* [Docker](https://docs.docker.com/engine/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### **Clone the repository**
```bash
git clone https://github.com/brian-1989/BGT_Pactual_project.git
cd Bgt_Pactual_project/
```

## **Use**
### **File .env**
Add the .env file, which stores the database credentials. This file was sent to the email address of the sender of the test. If you wish, you can also write to the developer of the test. The details are in the author.

### **Build the application images**
```bash
docker compose build --no-cache
````

### **Run the application by starting the containers**
```bash
docker compose up -d
````

### **Run Unit Tests**
```bash
pytest test/
````

## **Endpoints**

### - **Fund subscription**
1. **Description:** This endpoint creates a new subscription to a fund.
2. **Path:** /api/v1/subscribe_fund
3. **HTTP Method:** POST
4. **Usage Example:**
	- Subscription notification via Email
		```python
		# Request to subscribe to the fund.
		response = client.post(
		    "/subscribe_fund",
		    json={"fund_id": "123", "notification_type": "email"}
		)
		# Expected output: A JSON response indicating the success or failure of the fund subscription process. 
		```
		
	- Subscription notification via SMS
		```python
		# Request to subscribe to the fund.
		response = client.post(
		    "/api/v1/subscribe_fund",
		    json={"fund_id": "123", "notification_type": "sms"}
		)
		# Expected output: A JSON response indicating the success or failure of the fund subscription process.
		```

### - **Cancel the fund subscription**
1. **Description:** This endpoint cancels the fund subscription.
2. **Path:** /api/v1/cancel_fund
3. **HTTP Method:** POST
4. **Usage Example:**
	```python
	# Request to cancel the fund subscription.
	response = client.post(
	    "/api/v1/cancel_fund",
	    json={"fund_id": "123"}
	)
	# Expected output: A JSON response indicating the success or failure of the fund cancellation process. 
	````

### - **Get All Transactions**
1. **Description:** This endpoint retrieves all transactions made by the user.
2. **Path:** /api/v1/all_transactions
3. **HTTP Method:** GET
4. **Usage Example:**
	```python
	# Request to retrieve all transactions
	response = client.get(
	    "/api/v1/all_transactions"
	)
	# Expected output: A JSON response indicating all transactions.

## **Autor**  
:man_technologist: **Briayan Zapata Pino**  
* [LinkedIn](https://www.linkedin.com/in/briayan-zapata/)
