import http.server
import socketserver
import json
import threading
import subprocess
import os

PORT = 8080

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Adiciona cabeçalhos CORS para permitir requisições vindas do GitHub Pages
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == '/command':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                action = data.get('action')
                print(f"\n[COMANDO RECEBIDO] Ação: {action}")
                
                # Executa a ação localmente no PC de casa
                self.execute_local_action(action)
                
                response_data = {"status": "success", "message": f"Ação {action} executada com sucesso!"}
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
            except Exception as e:
                print(f"[ERRO] {str(e)}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def execute_local_action(self, action):
        try:
            import pyautogui
            if action == "next_slide":
                pyautogui.press('right')
                print(" -> Seta para a DIREITA pressionada no PC de casa.")
            elif action == "prev_slide":
                pyautogui.press('left')
                print(" -> Seta para a ESQUERDA pressionada no PC de casa.")
            elif action == "media_play_pause":
                pyautogui.press('playpause')
                print(" -> Play/Pause acionado no PC de casa.")
            elif action == "take_screenshot":
                screenshot = pyautogui.screenshot()
                filename = f"screenshot_home_{int(os.path.time()) if hasattr(os, 'time') else 0}.png"
                screenshot.save("screenshot_home.png")
                print(" -> Screenshot salva na pasta do servidor!")
        except ImportError:
            print(" -> [AVISO] Biblioteca 'pyautogui' não instalada. Instale com 'pip install pyautogui' para automações.")

def run_server():
    with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
        print(f"[*] Servidor rodando localmente na porta {PORT}...")
        httpd.serve_forever()

if __name__ == "__main__":
    print("=== SERVIDOR DE CONTROLE REMOTO (CASA) ===")
    print("Dica: Para expor este servidor para a internet e acessá-lo pelo GitHub Pages,")
    print("você pode usar uma ferramenta gratuita de túnel como o Localtunnel ou Ngrok:")
    print(f"Exemplo com Localtunnel (após instalar node.js): npx localtunnel --port {PORT}")
    print("-" * 50)
    
    # Inicia o servidor HTTP em uma thread separada
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Mantém o programa rodando
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
