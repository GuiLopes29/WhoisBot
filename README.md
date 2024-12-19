# WhoisBot

Um bot do Discord para verificar a disponibilidade de domínios.

## Requisitos

- Python 3.11 ou superior
- Discord API Token (configure no arquivo `.env`)

## Instalação

1. Clone o repositório:

    ```sh
    git clone https://github.com/GuiLopes29/WhoisBot.git
    cd WhoisBot
    ```

2. Crie e ative um ambiente virtual:

    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:

    ```sh
    pip install -r requirements.txt
    ```

4. Configure o arquivo `.env` com seu token do Discord e ID do canal:

    ```env
    DISCORD_TOKEN=seu-token-aqui
    DISCORD_CHANNEL=seu-channel-id-aqui
    ```

## Uso

Para iniciar o bot, execute:

```sh
python main.py
```
