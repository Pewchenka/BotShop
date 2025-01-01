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
