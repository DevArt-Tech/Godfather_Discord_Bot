# Godfather_Discord_Bot

## Comandos para ejecutar el bot:

Construimos la imagen

    docker build -t il-padrino-bot .

Ejecutamos el contenedor

    docker run -d -e discord_token=token -e discord_server_name=test --name il-padrino-della-famiglia il-padrino-bot