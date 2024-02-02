# Deploy a demo app to AWS ECS using AWS Copilot

## Prerequisites

- [AWS Copilot](https://aws.github.io/copilot-cli/)

### Installing on Ubuntu-based machines

```bash
curl -Lo copilot https://github.com/aws/copilot-cli/releases/latest/download/copilot-linux
chmod +x copilot
sudo mv copilot /usr/local/bin/copilot
copilot --help
```

## Deploy

```bash
# point your profile to the right AWS account
AWS_PROFILE=my-aws-account

copilot init --app mastering-docker --name web --env dev --type 'Load Balanced Web Service' --dockerfile ./Dockerfile --deploy
```
