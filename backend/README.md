<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../docs/pythoncerrado-2026-logo-dark.png">
    <img alt="Python Cerrado 2026" src="../docs/pythoncerrado-2026-logo-light.png" width="360">
  </picture>
</p>

# pythoncerrado.site

Backend do site da [Python Cerrado](https://pythoncerrado.org): instalação do Plone 6 e o pacote de política `pythoncerrado.site`.

## O que o pacote faz

- Instala e configura os add-ons do site: `collective.techevent`, `sc.voltolighttheme`, `sc.videos`, `plone.formblock` e `plonegovbr.socialmedia`.
- Registra os três temas da edição 2026 no painel **Temas** do `sc.voltolighttheme`:

  | Id | Nome | Cor de destaque |
  | --- | --- | --- |
  | `pythoncerrado-2026` | Python Cerrado 2026 (Vereda) | `#0f6b55` |
  | `pythoncerrado-2026-terra-vermelha` | Python Cerrado 2026 — Terra vermelha | `#b23a12` |
  | `pythoncerrado-2026-ipe` | Python Cerrado 2026 — Ipê | `#5b2a86` |

  Os valores ficam em [`themes.py`](./src/pythoncerrado/site/themes.py) e no registro do profile, em [`sc.voltolighttheme.themes.xml`](./src/pythoncerrado/site/profiles/default/registry/sc.voltolighttheme.themes.xml). Os testes conferem que os dois estão iguais.
  A edição `/2026` usa o tema Vereda; os outros dois ficam disponíveis para troca pelo painel, sem deploy.
  O registro de tema não guarda o logo: ao trocar de tema, troque também o logo de `/2026` pelo par correspondente em [`docs/`](../docs/).

- Traz o conteúdo de exemplo da edição 2026 (profile `pythoncerrado.site:initial`), em formato [`plone.exportimport`](https://github.com/plone/plone.exportimport), na pasta [`setuphandlers/examplecontent`](./src/pythoncerrado/site/setuphandlers/examplecontent/).

## Desenvolvimento

### Pré-requisitos ✅

-   Um [sistema operacional](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) que atenda aos requisitos abaixo.
-   [uv](https://6.docs.plone.org/install/create-project-cookieplone.html#uv)
-   [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
-   [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)
-   [Docker](https://docs.docker.com/get-started/get-docker/) (opcional)

### Instalação 🔧

1.  Clone o repositório e entre no diretório do backend.

    ```shell
    git clone git@github.com:plonegovbr/pythoncerrado-site.git
    cd pythoncerrado-site/backend
    ```

2.  Instale o Plone e as dependências.

    ```shell
    make install
    ```

3.  Crie o site Plone com o conteúdo de exemplo.

    ```shell
    make create-site
    ```

4.  Inicie o Plone em http://localhost:8080/.

    ```shell
    make start
    ```

### Conteúdo de exemplo

O conteúdo de exemplo é mantido num site local e exportado para dentro do pacote:

```shell
make update-example-content
```

### Testes e qualidade de código

```shell
make test
make format
make lint
```

Execute `make help` para ver todos os comandos disponíveis.

### Adicionando funcionalidades com `plonecli`

O pacote traz marcadores (`<!-- extra stuff goes here -->`) compatíveis com o [`plonecli`](https://github.com/plone/plonecli) e o [`bobtemplates.plone`](https://github.com/plone/bobtemplates.plone).
Eles permitem adicionar comportamentos, painéis de controle, tipos de conteúdo e outros subtemplates:

```shell
make add <template>
```

Por exemplo, `make add content_type` ou `make add behavior`.
A lista completa está no [README do `bobtemplates.plone`](https://github.com/plone/bobtemplates.plone/?tab=readme-ov-file#provided-subtemplates).

## Contribua

- [Issues](https://github.com/plonegovbr/pythoncerrado-site/issues)
- [Código-fonte](https://github.com/plonegovbr/pythoncerrado-site/)

## Licença

O projeto é distribuído sob a licença GPLv2.

## Créditos 🙏

Mantido pela comunidade [PloneGov-BR](https://plone.org.br).
Projeto gerado com [Cookieplone](https://github.com/plone/cookieplone) e [cookieplone-templates](https://github.com/plone/cookieplone-templates/).
