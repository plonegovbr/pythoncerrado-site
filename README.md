<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/pythoncerrado-2026-logo-dark.png">
    <img alt="Python Cerrado 2026" src="docs/pythoncerrado-2026-logo-light.png" width="420">
  </picture>
</p>

# Python Cerrado

[![Built with Cookieplone](https://img.shields.io/badge/built%20with-Cookieplone-0083be.svg?logo=cookiecutter)](https://github.com/plone/cookieplone-templates/)
[![CI](https://github.com/plonegovbr/pythoncerrado-site/actions/workflows/main.yml/badge.svg)](https://github.com/plonegovbr/pythoncerrado-site/actions/workflows/main.yml)

Site da [Python Cerrado](https://pythoncerrado.org), o encontro da comunidade Python do Centro-Oeste do Brasil.
A edição de 2026 acontece em **06 e 07 de novembro de 2026, em Brasília, DF**.

O site é feito com [Plone 6](https://plone.org) e [Volto](https://6.docs.plone.org/volto/).
Cada edição do evento é uma raiz de navegação do mesmo site (`/2026`, `/2025`, …), com logo e tema próprios.

## Início rápido 🏁

### Pré-requisitos ✅

-   Um [sistema operacional](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) que atenda aos requisitos abaixo.
-   [uv](https://6.docs.plone.org/install/create-project-cookieplone.html#uv)
-   [nvm](https://6.docs.plone.org/install/create-project-cookieplone.html#nvm)
-   [Node.js e pnpm](https://6.docs.plone.org/install/create-project.html#node-js) 24
-   [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
-   [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)
-   [Docker](https://docs.docker.com/get-started/get-docker/) (opcional)

### Instalação 🔧

1.  Clone o repositório e entre no diretório.

    ```shell
    git clone git@github.com:plonegovbr/pythoncerrado-site.git
    cd pythoncerrado-site
    ```

2.  Instale o backend e o frontend.

    ```shell
    make install
    ```

### Subindo os servidores 🔥

1.  Na primeira execução, crie o site Plone com o conteúdo de exemplo.

    ```shell
    make backend-create-site
    ```

2.  Inicie o backend em http://localhost:8080/.

    ```shell
    make backend-start
    ```

3.  Em outro terminal, inicie o frontend em http://localhost:3000/.

    ```shell
    make frontend-start
    ```

### Stack local com Docker 📦

O `docker-compose.yml` sobe um ambiente completo com:

- as imagens do backend e do frontend;
- um roteador Traefik e um servidor ZEO para o banco de dados;
- acesso em [http://pythoncerrado-site.localhost](http://pythoncerrado-site.localhost).

```shell
make stack-create-site
make stack-start
```

Use `make stack-status` para ver os serviços, `make stack-stop` para pará-los e `make stack-rm` para removê-los junto com os volumes.

## Estrutura do projeto 🏗️

Este monorepo tem as seguintes partes:

- **[backend](./backend/)**: instalação do Plone (com uv, sem buildout) e o pacote de política `pythoncerrado.site`, que configura o site, registra os temas da edição 2026 e traz o conteúdo de exemplo.
- **[frontend](./frontend/)**: o add-on Volto `volto-pythoncerrado-site`, que reúne o tema e os add-ons do site.
- **[devops](./devops/)**: a stack Docker de produção (`devops/stacks/pythoncerrado.org.yml`) e instruções para pipelines no GitLab.
- **[docs](./docs/)**: os logos da edição 2026 nas três variações de tema (Vereda, Terra vermelha e Ipê), em versões para fundo claro e escuro.

### Add-ons principais

| Parte | Add-on | Para quê |
| --- | --- | --- |
| backend | [`collective.techevent`](https://github.com/collective/tech-event) | Evento, grade, palestras, palestrantes e patrocinadores |
| backend | [`sc.voltolighttheme`](https://github.com/simplesconsultoria/sc-volto-light-theme) | Painel de temas, cabeçalho e rodapé configuráveis |
| frontend | [`@plone-collective/volto-techevent`](https://github.com/collective/tech-event) | Blocos e visões do tech-event |
| frontend | [`@simplesconsultoria/volto-light-theme`](https://github.com/simplesconsultoria/sc-volto-light-theme) | Tema baseado no `@kitconcept/volto-light-theme` |

## Qualidade de código 🧐

Para formatar o código e verificar se ele segue os padrões do projeto:

```shell
make check
```

`make check` executa `make format` e depois `make lint`. Os dois também podem ser executados separadamente, aqui ou dentro de `backend` e `frontend`.

| Parte | Ferramenta | Função | Configuração |
| --- | --- | --- | --- |
| backend | Ruff | Formatação e lint de Python, ordenação de imports | [`backend/pyproject.toml`](./backend/pyproject.toml) |
| backend | `zpretty` | Formatação de XML e ZCML | -- |
| backend | Pyroma | Metadados do pacote Python | -- |
| backend | check-python-versions | Versões de Python declaradas | -- |
| frontend | ESLint | Lint de JavaScript e TypeScript | [`frontend/.eslintrc.js`](./frontend/.eslintrc.js) |
| frontend | Prettier | Formatação de JavaScript e TypeScript | [`frontend/.prettierrc`](./frontend/.prettierrc) |
| frontend | Stylelint | Formatação de estilos (CSS, Less, Sass) | [`frontend/.stylelintrc`](./frontend/.stylelintrc) |

## Testes 🧪

```shell
make test
```

Executa os testes do backend (pytest) e do frontend (Vitest). Use `make backend-test` ou `make frontend-test` para rodar só uma das partes.

## Internacionalização 🌐

O site é publicado apenas em português do Brasil. Para atualizar os arquivos de tradução do Plone e do Volto:

```shell
make i18n
```

## Créditos 🙏

Mantido pela comunidade [PloneGov-BR](https://plone.org.br).

Projeto gerado com [Cookieplone (2.0.2)](https://github.com/plone/cookieplone) e [cookieplone-templates (19d0792)](https://github.com/plone/cookieplone-templates/commit/19d07923b43f38bc80271aab3d4ea54388fa9d23) em 13/10/2026.
