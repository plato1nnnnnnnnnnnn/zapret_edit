import json
from handlers import discord, youtube, soundcloud, spotify

# Загрузка конфигурации
with open('src/config.json', 'r') as f:
    config = json.load(f)

ENABLED_SERVICES = config.get('enabled_services', [])


# Словарь доменов для сервисов
SERVICE_DOMAINS = {
    'discord': ['discord.com', 'cdn.discordapp.com'],
    'youtube': ['youtube.com', 'youtu.be', 'googlevideo.com'],
    'soundcloud': ['soundcloud.com'],
    'spotify': ['spotify.com', 'audio-ak.spotify.com']
}

def detect_service_by_domain(domain):
    for service, domains in SERVICE_DOMAINS.items():
        if any(domain.endswith(d) for d in domains):
            return service
    return None

def process_packet(packet):
    # packet должен содержать поле 'domain' (или аналогичное)
    domain = packet.get('domain', '')
    service_name = detect_service_by_domain(domain)
    if service_name and service_name in ENABLED_SERVICES:
        if service_name == 'discord':
            discord.handle_discord_traffic(packet)
        elif service_name == 'youtube':
            youtube.handle_youtube_traffic(packet)
        elif service_name == 'soundcloud':
            soundcloud.handle_soundcloud_traffic(packet)
        elif service_name == 'spotify':
            spotify.handle_spotify_traffic(packet)
    else:
        pass  # Остальной трафик не обрабатывается

# TODO: Реализовать реальный перехват сетевого трафика и передачу в process_packet
