#!/bin/bash

SCRIPT_SRC="./fckeditor_checker_v0_1.py"
INSTALL_DIR="/usr/local/bin"
CMD_NAME="fckupload"

if [ ! -f "$SCRIPT_SRC" ]; then
  echo "[!] Arquivo $SCRIPT_SRC não encontrado. Coloque o setup.sh na mesma pasta do script ou ajuste o caminho."
  exit 1
fi
echo "[!] USE COM RESPONSABILIDADE"

echo "[*] Instalando dependência requests via pip (ignorando avisos)..."
pip3 install --user --upgrade --disable-pip-version-check requests > /dev/null 2>&1

sudo cp "$SCRIPT_SRC" "$INSTALL_DIR/$CMD_NAME.py"
sudo chmod +x "$INSTALL_DIR/$CMD_NAME.py"

echo "#!/bin/bash
python3 $INSTALL_DIR/$CMD_NAME.py \"\$@\"
" | sudo tee "$INSTALL_DIR/$CMD_NAME" > /dev/null

sudo chmod +x "$INSTALL_DIR/$CMD_NAME"

echo "[+] Instalado com sucesso!"
echo "[+] Agora você pode usar o comando '$CMD_NAME' em qualquer lugar."
