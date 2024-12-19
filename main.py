"""
WhoisBot: Um bot do Discord para verificar a disponibilidade de domínios.
"""

import os
import sys
import asyncio
import logging

import discord
from whois import whois, parser
from dotenv import load_dotenv

# Configurar o logger para gravar em um arquivo
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("whois_bot.log"),
        logging.StreamHandler()
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
            return "Disponível"

        # Limpar os links dos status
        status_str = ", ".join([status.split(" ")[0] for status in w.status])
        logger.info("Status do domínio %s: %s", dominio, status_str)
        return status_str

    except parser.PywhoisError:
        logger.info("Domínio %s não encontrado.", dominio)
        return "Disponível"
    except Exception as e:
        # Justificativa: Captura ampla de exceções para garantir a robustez do código.
        logger.error("Erro ao consultar WHOIS para %s: %s", dominio, e)
        return f"Erro: {e}"

async def loop_verificacao():
    """
    Loop contínuo que verifica os domínios e envia o status para o canal do Discord.
    """
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        logger.error("Canal com ID %d não encontrado. Verifique o .env.", CHANNEL_ID)
        return

    dominios = ["solutech.dev", "nandomain.dev"]
    while True:
        for dominio in dominios:
            try:
                status = await verificar_dominio(dominio)
                if status:
                    await channel.send(
                        f"Status do domínio **{dominio}**: {status}"
                    )
                else:
                    await channel.send(
                        f"Não foi possível verificar o domínio **{dominio}**."
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
            except discord.DiscordException as e:
                logger.error(
                    "Erro inesperado no loop de verificação para %s: %s", dominio, e
                )
                await channel.send(
                    f"Ocorreu um erro ao verificar {dominio}. Contate um administrador."
                )
            except Exception as e:
                # Justificativa: Captura ampla de exceções para garantir a robustez do código.
                logger.error(
                    "Erro inesperado no loop de verificação para %s: %s", dominio, e
                )
                await channel.send(
                    f"Ocorreu um erro ao verificar {dominio}. Contate um administrador."
                )

        await asyncio.sleep(60 * 60)

@client.event
async def on_ready():
    logger.info('%s está conectado ao Discord!', client.user)
    logger.info("Conectado ao canal: %s", client.get_channel(CHANNEL_ID))
    client.loop.create_task(loop_verificacao())

client.run(TOKEN)
