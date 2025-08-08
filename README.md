# FCKEditor Checker

Ferramenta em Python para automatizar a detecção da vulnerabilidade de upload arbitrário de arquivos ASP em servidores que utilizam o componente FCKeditor.

---

## Requisitos

* Python 3.x
* Biblioteca `requests`

Instale a dependência com:

```bash
pip install requests
```

---

## Uso

```bash
python fckeditor_checker_v0_1.py <base_url> [opções]
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
python fckeditor_checker_v0_1.py http://example.com/app/
```

Testando com arquivo personalizado e sem fallback:

```bash
python fckeditor_checker_v0_1.py http://example.com/app/ --filename shell.asp --type File --no-follow-fallback
```

---

## Aviso Legal

Use esta ferramenta **APENAS em sistemas para os quais você tem autorização explícita para testes de segurança**. O uso não autorizado é ilegal e antiético.

---

## Autor

Desenvolvido por jgbiispo
