# BotShop
## Usage
Just add  bot https://t.me/listpokup_bot in your telegram group and ajust admin privelegies  

## Development
Secrets must be stored in `.env`  which s  not part of repository (see `.env.example`)
For local development use `docker compose`
```bash
docker compose --profile local up
```

if you want to rebuild image use `--build` flag
```bash
docker compose --profile local up --build
```
### AWS Deployment
```shell
$ # Copy secrets and compose to remote server  from **root project folder**
$ scp ./docker-compose.yaml ubuntu@13.251.202.135:~/botlist
$ scp ./.env ubuntu@13.251.202.135:~/botlist 


$ # In manual mode
$ ssh ubuntu@13.251.202.135
$ docker compose --profile aws up -d

$ # one local command
$ ssh ubuntu@13.251.202.135 "cd botlist;docker compose --profile aws up -d"
```
Usefull link about AWS and github integration:   
https://loisthash.medium.com/ci-cd-from-github-to-aws-ec2-667e6c4f4ffc  
https://aws.amazon.com/blogs/devops/integrating-with-github-actions-ci-cd-pipeline-to-deploy-a-web-app-to-amazon-ec2/
