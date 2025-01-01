# BotShop

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
ssh ubuntu@13.251.202.135

scp ./docker-compose.yaml ubuntu@13.251.202.135:~/botlist
scp ./.env ubuntu@13.251.202.135:~/botlist 
```