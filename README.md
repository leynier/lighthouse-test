# Lighthouse Technical Test

- Install **AWS CLI** if not already installed: <https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html>
- Install **AWS CDK** if not already installed: <https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html>
- Install **Docker** if not already installed: <https://docs.docker.com/get-docker>
- Install **uv** if not already installed: <https://docs.astral.sh/uv/getting-started/installation>
- Install **Make** if not already installed: <https://www.gnu.org/software/make>
- Login to AWS CLI if not already logged in: `aws configure`
- Clone this repository and navigate to the root of the project
- Execute `make install` to install the Python dependencies
- Execute `make bootstrap` to bootstrap the AWS CDK (**IMPORTANT:** only needed once per AWS account)
- Execute `make deploy` to deploy the AWS CDK stack
- Create a `.env` file in the root of the project with the `API_GATEWAY_URL` variable set to the API Gateway URL
  > The API Gateway URL will be printed in the console after the deployment is complete when executing `make deploy`
- Execute `make test` to run the integration tests
- Execute `make destroy` to destroy the AWS CDK stack
