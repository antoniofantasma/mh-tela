# Controle Remoto Direto (GitHub Pages + Servidor Local)

Esta arquitetura utiliza um servidor Python leve rodando no seu PC de casa conectado a um túnel público gratuito. A página web hospedada no GitHub Pages se comunica diretamente com o seu PC, sem precisar de tokens do GitHub.

## Como Funciona:
1. **No seu PC de casa:** Você roda o `server.py` e abre um túnel público gratuito (ex: `localtunnel` ou `ngrok`) para gerar um link público temporário (ex: `https://xxxx.loca.lt`).
2. **No GitHub Pages:** Você hospeda o `index.html`. No painel do site, você cola esse link gerado pelo seu PC de casa.
3. **No PC da empresa:** Você abre o site do GitHub Pages, clica nos botões e o comando vai direto em tempo real para o seu PC de casa via túnel!

---

## Passo a Passo:

### 1. No seu PC de casa:
1. Instale o Python (caso não tenha) e a biblioteca de automação:
   ```bash
   pip install pyautogui
   ```
2. Execute o servidor Python:
   ```bash
   python server.py
   ```
3. Para expor o servidor para a internet de forma gratuita e sem complicação, abra outro terminal e use o **Localtunnel** (requer Node.js instalado) ou o **Ngrok**:
   - Com Localtunnel:
     ```bash
     npx localtunnel --port 8080
     ```
   - O comando vai te retornar uma URL pública (ex: `https://empty-dogs-jump.loca.lt`). Copie essa URL.

### 2. No GitHub:
1. Faça upload do arquivo `index.html` (da pasta `frontend/`) para o seu repositório do GitHub Pages.

### 3. Usando no PC da Empresa:
1. Acesse a URL do seu GitHub Pages.
2. No campo **URL do Servidor / Túnel**, cole o link gerado pelo seu PC de casa (ex: `https://empty-dogs-jump.loca.lt`).
3. Clique nos botões de controle! O comando será executado instantaneamente no seu PC de casa.
