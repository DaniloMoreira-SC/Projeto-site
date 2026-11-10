# PRD — Vice City Dossier

## Problema original
Criar, a partir dos arquivos HTML/CSS/JS enviados, uma experiência sobre GTA VI com menu hamburguer, história, personagens com troca visual, easter eggs e carrossel de trailers.

## Decisões de arquitetura
- Frontend React com Framer Motion, Lenis, Lucide e CSS autoral neon tropical.
- Backend FastAPI com endpoints locais em `/api/story`, `/api/characters`, `/api/easter-eggs` e `/api/trailers`.
- Dados editoriais estáticos nos endpoints, sem dependência de serviço externo ou autenticação.
- Imagens e referências visuais baseadas nos artefatos enviados e na direção Vice City definida para o produto.

## Implementado
- Hero cinético com reveal de linhas, imagem tratada, assinatura VCVI e marquee editorial.
- Menu hamburguer animado com navegação por seções.
- História editorial em capítulos, com teorias identificadas.
- Seletor visual de Lucia e Jason, incluindo estado ativo e personagem futuro.
- Mapa visual de easter eggs com filtros por categoria e cards interativos.
- Carrossel de trailers com navegação, imagem, título, duração e progresso.
- Status de sincronização da API e fallback visual para carregamento.
- Responsividade desktop/mobile e validação dos fluxos principais.

## Backlog priorizado
- P0: manter conteúdo oficial atualizado quando novos materiais forem publicados.
- P1: adicionar mais personagens e capítulos ao arquivo editorial.
- P1: substituir cards de trailer por embeds oficiais quando as URLs estiverem disponíveis.
- P2: adicionar persistência de easter eggs marcados como favoritos.