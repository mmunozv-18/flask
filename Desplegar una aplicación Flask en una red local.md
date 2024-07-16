Para desplegar una aplicación Flask en una red local, necesitas un servidor web capaz de manejar las solicitudes de manera eficiente. Aunque Flask incluye un servidor de desarrollo integrado (`flask run`), no se recomienda para producción. En su lugar, puedes usar servidores web como Gunicorn o uWSGI junto con un servidor proxy inverso como Nginx.

**Pasos para desplegar una aplicación Flask en tu red local usando Gunicorn y Nginx:**

1. **Instala Gunicorn:**
   Gunicorn es un servidor WSGI para aplicaciones Python. Puedes instalarlo usando pip:
   
   ```bash
   pip install gunicorn
   ```

2. **Crea tu aplicación Flask:**
   Supongamos que tienes una aplicación llamada `app.py`:
   
   ```python
   # app.py
   from flask import Flask
   
   app = Flask(__name__)
   
   @app.route('/')
   def hello():
       return "Hello, World!"
   
   if __name__ == '__main__':
       app.run()
   ```

3. **Inicia Gunicorn:**
   Inicia Gunicorn para servir tu aplicación Flask. Supongamos que tu aplicación se llama `app:app` (archivo `app.py`, objeto `app`).
   
   ```bash
   gunicorn --bind 0.0.0.0:8000 app:app
   ```
   
   Esto iniciará Gunicorn sirviendo tu aplicación en el puerto 8000.

4. **Instala y configura Nginx:**
   Nginx actuará como un proxy inverso para Gunicorn.
   
   - Instala Nginx:
   
   ```bash
   sudo apt-get update
   sudo apt-get install nginx
   ```
   
   - Configura un nuevo archivo para tu aplicación Flask.
   
   Crea un archivo de configuración en `/etc/nginx/sites-available/`:
   
   ```bash
   sudo nano /etc/nginx/sites-available/flask_app
   ```
   
   Y añade el siguiente contenido:
   
   ```nginx
   server {
       listen 80;
       server_name tu_direccion_ip_local;
   
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   
       error_log /var/log/nginx/flask_app_error.log;
       access_log /var/log/nginx/flask_app_access.log;
   }
   ```
   
   - Habilita el archivo de configuración:
   
   ```bash
   sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/
   ```
   
   - Prueba la configuración de Nginx:
   
   ```bash
   sudo nginx -t
   ```
   
   - Reinicia Nginx:
   
   ```bash
   sudo systemctl restart nginx
   ```

5. **Ajusta las reglas del firewall (si es necesario):**
   Si estás usando `ufw` (firewall de Ubuntu), permite el tráfico HTTP:
   
   ```bash
   sudo ufw allow 'Nginx Full'
   ```

6. **Accede a tu aplicación:**
   Ahora deberías poder acceder a tu aplicación Flask en tu red local a través de `http://tu_direccion_ip_local`.

**Notas Adicionales:**

- **Supervisar Gunicorn con Systemd:**
  Para asegurarte de que Gunicorn se reinicie automáticamente y esté siempre activo, puedes configurarlo como un servicio de `systemd`.
  Crea un archivo de servicio para Gunicorn:
  
  ```bash
  sudo nano /etc/systemd/system/gunicorn.service
  ```
  
  Añade el siguiente contenido, ajustando el usuario, el grupo y las rutas según sea necesario:
  
  ```ini
  [Unit]
  Description=Gunicorn instance to serve Flask
  After=network.target
  
  [Service]
  User=tu_usuario
  Group=www-data
  WorkingDirectory=/ruta/a/tu/proyecto
  ExecStart=/ruta/a/tu/entorno/virtual/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 app:app
  
  [Install]
  WantedBy=multi-user.target
  ```
  
  Luego, recarga los servicios de `systemd`, inicia el servicio Gunicorn y habilítalo para que se ejecute al iniciar:
  
  ```bash
  sudo systemctl daemon-reload
  sudo systemctl start gunicorn
  sudo systemctl enable gunicorn
  ```

Siguiendo estos pasos, tu aplicación Flask estará lista para ser accedida en una red local con un proxy inverso y un servidor WSGI.
