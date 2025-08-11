#!/bin/bash

SCRIPT_SRC="./fckeditor.py"

INSTALL_DIR="/usr/local/bin"

CMD_NAME="fckupload"

if [ ! -f "$SCRIPT_SRC" ]; then
  echo "[!] Arquivo $SCRIPT_SRC não encontrado. Coloque o setup.sh na mesma pasta do script ou ajuste o caminho."
  exit 1
fi
echo "[!] USE COM RESPONSABILIDADE"
echo "[*] Instalando dependência requests via pip..."
pip3 install --upgrade --disable-pip-version-check requests > /dev/null 2>&1
pip3 install --upgrade --disable-pip-version-check colorama > /dev/null 2>&1

sudo cp "$SCRIPT_SRC" "$INSTALL_DIR/$CMD_NAME.py"
sudo chmod +x "$INSTALL_DIR/$CMD_NAME.py"

echo "#!/bin/bash
python3 $INSTALL_DIR/$CMD_NAME.py \"\$@\"
" | sudo tee "$INSTALL_DIR/$CMD_NAME" > /dev/null

sudo chmod +x "$INSTALL_DIR/$CMD_NAME"

echo "[+] Instalado com sucesso!"
echo "[+] Agora você pode usar o comando '$CMD_NAME' em qualquer lugar."
