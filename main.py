"""
Este módulo contém um bot do Discord que verifica o status de domínios usando WHOIS.
"""

import os
import sys
import asyncio
import logging
from socket import timeout as socket_timeout

import discord
from whois import whois, parser
from dotenv import load_dotenv

# Configurar o logger para gravar em um arquivo e no console com codificação UTF-8
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("whois_bot.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('DISCORD_CHANNEL')

# Verificar se as variáveis de ambiente foram carregadas corretamente
if TOKEN is None or CHANNEL_ID is None:
    logger.error("Variáveis de ambiente TOKEN ou CHANNEL_ID não definidas.")
    sys.exit(1)

CHANNEL_ID = int(CHANNEL_ID)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def verificar_dominio(dominio):
    """
    Verifica o status do domínio usando WHOIS.
    """
    try:
        w = whois(dominio)
        if not w or not w.status:
            logger.info("Domínio %s disponível!", dominio)
            return "✅ Disponível"

        # Limpar os links dos status
        if isinstance(w.status, list):
            status_str = ", ".join(
                [status.split(" ")[0] for status in w.status if "http" not in status]
            )
        else:
            status_str = w.status.split(" ")[0]

        logger.info("Status do domínio %s: %s", dominio, status_str)
        return f"❌ {status_str}"

    except parser.PywhoisError:
        logger.info("Domínio %s não encontrado.", dominio)
        status = "✅ Disponível"
    except AttributeError as e:
        logger.error("Erro ao consultar WHOIS para %s: %s", dominio, e)
        status = f"❌ Erro: {e}"
    except (ValueError, TypeError, RuntimeError, socket_timeout) as e:
        logger.error("Erro ao consultar WHOIS para %s: %s", dominio, e)
        status = f"❌ Erro: {e}"
    except (ConnectionError, OSError) as e:
        logger.error("Erro de conexão ao consultar WHOIS para %s: %s", dominio, e)
        status = "Erro de conexão"

    return status

async def loop_verificacao():
    """
    Loop contínuo que verifica os domínios e envia o status para o canal do Discord.
    """
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        logger.error("Canal com ID %d não encontrado. Verifique o .env.", CHANNEL_ID)
        return

    dominios = ["nandomain.dev"]
    dominios = ["solutech.dev"]
    while True:
        for dominio in dominios:
            try:
                status = await verificar_dominio(dominio)
                if status == "Erro de conexão":
                    await channel.send(
                        f"Erro de conexão ao verificar o domínio **{dominio}**. "
                        "Tentando novamente em 1 minuto."
                    )
                    await asyncio.sleep(60)
                    continue

                await channel.send(
                    f"Status do domínio **{dominio}**: {status}"
                )
            except discord.errors.HTTPException as e:
                logger.error("Erro ao enviar mensagem para o Discord: %s", e)
                if e.code == 50035:
                    await channel.send(
                        f"A resposta para {dominio} é muito longa para o Discord."
                    )
                else:
                    await channel.send(
                        f"Ocorreu um erro ao verificar {dominio}. Tente novamente mais tarde."
                    )
                await asyncio.sleep(60)
            except discord.DiscordException as e:
                logger.error(
                    "Erro inesperado no loop de verificação para %s: %s", dominio, e
                )
                await channel.send(
                    f"Ocorreu um erro ao verificar {dominio}. Contate um administrador."
                )
                await asyncio.sleep(60)
            except (ValueError, TypeError, RuntimeError, socket_timeout) as e:
                logger.error(
                    "Erro inesperado no loop de verificação para %s: %s", dominio, e
                )
                await channel.send(
                    f"Ocorreu um erro ao verificar {dominio}. Contate um administrador."
                )
                await asyncio.sleep(60)
            except (ConnectionError, OSError) as e:
                logger.error(
                    "Erro de conexão no loop de verificação para %s: %s", dominio, e
                )
                await channel.send(
                    f"Ocorreu um erro de conexão ao verificar {dominio}. Contate um administrador."
                )
                await asyncio.sleep(60)

        await asyncio.sleep(60 * 60)

@client.event
async def on_ready():
    """
    Evento que é acionado quando o bot está pronto para uso.
    """
    logger.info('%s está conectado ao Discord!', client.user)
    logger.info("Conectado ao canal: %s", client.get_channel(CHANNEL_ID))
    client.loop.create_task(loop_verificacao())

client.run(TOKEN)
