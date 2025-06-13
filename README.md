===============================
Sistema de Check-in com QR Code
===============================

Este é um sistema web desenvolvido com Python e Flask para registrar participantes de eventos e realizar o check-in presencial via leitura de QR Code.

-------------------------------
Funcionalidades
-------------------------------
✔ Registro de participantes com nome e e-mail  
✔ Geração automática de QR Code único por participante  
✔ Leitura do QR Code via webcam usando a câmera do navegador  
✔ Validação do check-in e registro da data/hora  
✔ Exportação dos participantes em CSV  
✔ Painel administrativo com login e proteção de sessão  
✔ Interface responsiva e adaptada para uso em dispositivos móveis  

-------------------------------
Tecnologias utilizadas
-------------------------------
- Python 3.x  
- Flask 3.x  
- Flask-Session  
- SQLite  
- QRCode (qrcode + pillow)  
- OpenCV (caso queira capturar imagens via webcam com Python)  
- pyzbar (para decodificar QR Codes - opcional)  
- html5-qrcode (biblioteca JS para leitura de QR no navegador)

-------------------------------
Como executar o projeto
-------------------------------

1. **Clone o projeto ou extraia o ZIP**
2. Crie e ative um ambiente virtual:

   Windows:
   > python -m venv venv  
   > venv\\Scripts\\activate

   Linux/Mac:
   $ python3 -m venv venv  
   $ source venv/bin/activate

3. **Instale as dependências**:
   > pip install -r requirements.txt

4. **Garanta que o banco está configurado corretamente**:
   - Rode `init_db.py` ou `ajustar_colunas.py` se necessário.

5. **Execute o app**:
   > python app.py

6. **Acesse no navegador**:
   http://127.0.0.1:5000

-------------------------------
Acesso ao Painel
-------------------------------

- Acesse: http://127.0.0.1:5000/login  
- Senha padrão: `admin123`

-------------------------------
Pastas importantes
-------------------------------

- `/static/qr_codes` → onde os QR Codes são gerados e salvos  
- `/templates/` → contém os arquivos HTML usados nas páginas

-------------------------------
Recomendações
-------------------------------

- Mantenha o ambiente virtual ativado para evitar conflitos de pacotes.
- Para uso em produção, troque a `secret_key` e implemente autenticação com usuários reais.

-------------------------------
Créditos
-------------------------------

Desenvolvido como projeto final do curso CS50.  
Componente de leitura de QR: html5-qrcode (https://github.com/mebjas/html5-qrcode)

