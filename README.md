# FCKEditor ASP Upload Vulnerability Checker

Ferramenta em Python para automatizar a detecção da vulnerabilidade de upload arbitrário de arquivos ASP em servidores que utilizam o componente FCKeditor.

---

## Requisitos

* Python 3.x

## Instalação

Para facilitar a execução da ferramenta de qualquer lugar no sistema, você pode usar o script `setup.sh` para instalar o comando personalizado.

### Passos:

1. Coloque o arquivo `setup.sh` na mesma pasta do script Python `fckeditor_checker_v0_1.py`.

2. Dê permissão executável para o script de instalação:

```bash
chmod +x setup.sh
```

3. Execute o script de instalação com permissão sudo:

```bash
sudo ./setup.sh
```

O comando padrão para executar será `fckupload`.

---

## Uso

Após instalação, execute a ferramenta em qualquer lugar usando:

```bash
fckupload <base_url> [opções]
```

### Parâmetros

* `<base_url>`: URL base do alvo (ex: `http://example.com/` ou `http://example.com/app/`)

### Opções

| Opção                  | Descrição                                                                              | Padrão              |
| ---------------------- | -------------------------------------------------------------------------------------- | ------------------- |
| `--filename <nome>`    | Nome do arquivo ASP a ser enviado. Se omitido, é gerado um nome único automaticamente. | `probe_<token>.asp` |
| `--type <valor>`       | Valor do parâmetro `Type` na requisição de upload (ex: `Media`, `File`)                | `Media`             |
| `--timeout <segundos>` | Tempo máximo para aguardar respostas HTTP                                              | 10                  |
| `--no-follow-fallback` | Não tenta buscar o arquivo em diretórios comuns padrão do FCKeditor                    | Desativado          |

---

## Exemplo

Testando o alvo `http://example.com/app/` com o parâmetro `Type=Media` (padrão):

```bash
fckupload http://example.com/app/
```

Testando com arquivo personalizado e sem fallback:

```bash
fckupload http://example.com/app/ --filename shell.asp --type File --no-follow-fallback
```

---

## Aviso Legal

Use esta ferramenta **APENAS em sistemas para os quais você tem autorização explícita para testes de segurança**. O uso não autorizado é ilegal e antiético.

---

## Autor

Desenvolvido por jgbiispo
