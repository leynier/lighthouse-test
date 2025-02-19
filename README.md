# Lighthouse Technical Test

This repository contains a technical test designed to assess your ability to develop **serverless backend applications in Python** using **AWS CDK** while following best practices. The test includes deploying **AWS Lambda functions** accessible via **API Gateway** and integrating them with a **DynamoDB table** for data storage.

## 🚀 Prerequisites

Make sure you have the following tools installed before proceeding:

| Tool  | Installation |
|-------------|------------|
| **AWS CLI** | [Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) |
| **AWS CDK** | [Installation Guide](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) |
| **Docker** | [Installation Guide](https://docs.docker.com/get-docker) |
| **uv** (Python dependency manager) | [Installation Guide](https://docs.astral.sh/uv/getting-started/installation) |
| **Make** | [Installation Guide](https://www.gnu.org/software/make) |

## 🔧 Setup

1. **Log in to AWS CLI** (if not already logged in):

   ```sh
   aws configure
   ```

2. **Clone this repository and navigate to the project root:**

   ```sh
   git clone https://github.com/leynier/lighthouse-test.git
   cd lighthouse-test
   ```

3. **Install Python dependencies:**

   ```sh
   make install
   ```

4. **Bootstrap AWS CDK** (only needed once per AWS account):

   ```sh
   make bootstrap
   ```

## 🚀 Deployment

To deploy the infrastructure on AWS, run:

```sh
make deploy
```

📌 **Note:** Once the deployment is complete, the API Gateway URL will be printed in the console.

## 📄 Environment Configuration

After deployment, create a `.env` file in the project root and set the API Gateway URL:

```ini
API_GATEWAY_URL=<API_GATEWAY_URL>
```

📌 **Replace `<API_GATEWAY_URL>` with the URL printed in the console after running `make deploy`.**

## ✅ Running Tests

To execute the integration tests, run:

```sh
make test
```

## ❌ Destroying the Infrastructure

To remove all deployed AWS resources, run:

```sh
make destroy
```
