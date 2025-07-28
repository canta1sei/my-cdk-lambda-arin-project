# My CDK Lambda A-rin Project

This project demonstrates how to build and deploy an AI chatbot using AWS CDK, Python Lambda, and Amazon Bedrock.
It covers end-to-end setup from custom VPC to Lambda function deployment.

## Technologies Used:
- AWS CDK (Python)
- AWS Lambda
- Amazon Bedrock (Claude model)
- AWS VPC, Subnet, Internet Gateway, Route Tables
- Python 3.9+
- pipenv

## Project Structure:
- `A-rin_lambda/A-rinApp.py`: The core Lambda function code for the chatbot.
- `my_cdk_lambda_project/my_cdk_lambda_project_stack.py`: CDK stack definition for deploying Lambda and IAM roles.

## Setup & Deployment:
1.  **VPC and EC2 Setup**: Configured a custom VPC, public subnet, Internet Gateway, and an EC2 instance (`t2.small`) with an appropriate IAM role.
2.  **CDK Environment Setup**: Installed Node.js, npm, pipenv, AWS CDK CLI on the EC2 instance.
3.  **CDK Bootstrap**: Ran `cdk bootstrap` to prepare the AWS environment.
4.  **Lambda Deployment**: Used `cdk deploy` to deploy the Lambda function and associated IAM roles.

## Troubleshooting Log: (For Findy & Blog)

This project encountered several challenges during setup and deployment. Documenting these issues and their resolutions to showcase problem-solving skills.

### 1. CDK Bootstrap IAM Permission Error
- **Error**: `AccessDenied` for `ecr:SetRepositoryPolicy`, SSM Parameter Store.
- **Cause**: Insufficient permissions on the attached EC2 IAM role (`cdk-dev-instance-role`).
- **Resolution**: Added `AdministratorAccess` managed policy to `cdk-dev-instance-role`.

### 2. `pip: command not found`
- **Error**: `-bash: pip: command not found` during `pip install pipenv`.
- **Cause**: `pip` was not installed by default on Amazon Linux 2023.
- **Resolution**: Ran `sudo yum install python3-pip -y`.

### 3. `cdk synth` `--app is required` Error
- **Error**: `--app is required...`
- **Cause**: Executing `cdk synth` from a subdirectory, not the project root.
- **Resolution**: Navigated to `/home/ec2-user/my-cdk-lambda-project`.

### 4. `cdk synth` `ModuleNotFoundError: No module named 'aws_cdk'`
- **Error**: Python `ModuleNotFoundError`.
- **Cause**: Python virtual environment (`.venv`) was not active or CDK libraries not installed within it.
- **Resolution**: Activated virtual environment (`source .venv/bin/activate`) and ran `pip install -r requirements.txt`.

### 5. Git Authentication Failed (`Password authentication is not supported`)
- **Error**: `remote: Invalid username or token. Password authentication is not supported for Git operations.`
- **Cause**: GitHub no longer supports password authentication for Git operations; Personal Access Token (PAT) is required.
- **Resolution**: Generated a PAT with `repo` scope on GitHub, and configured Git to use it by embedding it in the remote URL: `git remote set-url origin https://canta1sei:YOUR_PAT@github.com/canta1sei/my-cdk-lambda-arin-project.git`.

### 6. `fatal: repository 'https://github.com/cantatsei/my-cdk-lambda-arin-project.git/' not found`
- **Error**: Repository not found despite correct URL, often after PAT embedding attempt.
- **Cause**: Typo in the username within the repository path in the URL (e.g., `github.com/cantatsei/...` instead of `github.com/canta1sei/...`).
- **Resolution**: Ensured the GitHub username in the URL's path matched the one in the authentication part: `https://canta1sei:YOUR_PAT@github.com/canta1sei/my-cdk-lambda-arin-project.git`.

### 7. Git Push Rejected (`remote contains work you do not have locally`)
- **Error**: `! [rejected] main -> main (fetch first)` because remote contains changes (e.g., auto-generated README/gitignore).
- **Cause**: Local and remote histories diverged (local had initial CDK commit, remote had auto-generated files).
- **Resolution**: Pulled remote changes with `git pull origin main --allow-unrelated-histories --no-rebase` and resolved merge conflicts (specifically in `.gitignore` and `README.md`).

### Next Steps:
- Resolve `KeyError: 'sessionState'` in Lambda function.
- Complete Lambda function testing.
- Consider adding API Gateway for external access.
- Finalize `README.md` content and add screenshots.
- Clean up AWS resources after project completion.
