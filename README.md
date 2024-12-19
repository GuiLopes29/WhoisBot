<div align="center">
    
# WhoisBot

Um bot do Discord para verificar a disponibilidade de domínios.

<img src="https://github.com/user-attachments/assets/1747dbaf-459c-402b-8944-cfaf25aa11c6" alt="WhoisBot Logo" width="200"/>

## Requisitos

 Python 3.11 ou superior
 Discord API Token (configure no arquivo `.env`)

## Instalação

 1º Clone o repositório:

    ```sh
    git clone https://github.com/GuiLopes29/WhoisBot.git
    cd WhoisBot
    ```

2º Crie e ative um ambiente virtual:

    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3º Instale as dependências:

    ```sh
    pip install -r requirements.txt
    ```

4º Configure o arquivo `.env` com seu token do Discord e ID do canal:

    ```env
    DISCORD_TOKEN=seu-token-aqui
    DISCORD_CHANNEL=seu-channel-id-aqui
    ```

## Uso

Para iniciar o bot, execute:

```sh
python seu_script.py
```
