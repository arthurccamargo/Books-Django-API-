# Book API

![Badge](https://img.shields.io/badge/Django-REST%20Framework-green)
![Badge](https://img.shields.io/badge/Status-Complete-brightgreen)

## Visão Geral

A **Book API** é uma API RESTful desenvolvida em Django REST Framework para gerenciar informações de livros e suas avaliações. O projeto inclui funcionalidades avançadas como autenticação com JWT, integração com a API do Google Books, exportação de dados, paginação, testes automatizados e documentação OpenAPI Swagger. Projetada com boas práticas, a API é ideal para demonstrar habilidades em desenvolvimento back-end.

---

## Funcionalidades Principais
- **Gerenciamento de Livros**:
  - Listagem, busca, criação, atualização e exclusão de livros.
  - Integração com a API do Google Books para buscar livros e salvar no banco de dados.

- **Sistema de Avaliações**:
  - Permite que os usuários avaliem os livros com notas e comentários.
  - Filtragem de avaliações por título e autor do livro.

- **Autenticação**:
  - Autenticação JWT (JSON Web Token) para proteger métodos sensíveis (`POST`, `PUT` e `DELETE`).
  - Métodos `GET` são acessíveis sem autenticação.

- **Paginação**:
  - Resultados organizados em páginas para maior eficiência e usabilidade.

- **Exportação de Dados**:
  - Possibilidade de exportar informações de livros e avaliações no formato CSV.

- **Organização em ViewSets**:
  - Estrutura modular e organizada para maior clareza e manutenção do código.

- **Documentação OpenAPI**:
  - Documentação detalhada integrada usando Swagger, facilitando o uso da API.

- **Testes Automatizados**:
  - Testes para endpoints e funcionalidades principais, garantindo a qualidade do código.

---

## Tecnologias Utilizadas

- **Django**
- **Django REST Framework**
- **SQLite** (Banco de dados padrão)
- **JWT** (para autenticação segura)

---

## Instalação

### Pré-requisitos

- Python 3.10 ou superior
- Git
- Virtualenv

## Utilização

### Endpoints Principais

#### Livros
- Listar livros: `GET /api/books/`
- Detalhar livro: `GET /api/books/{id}/`
- Criar livro: `POST /api/books/` (requer autenticação)
- Atualizar livro: `PUT /api/books/{id}/` (requer autenticação)
- Deletar livro: `DELETE /api/books/{id}/` (requer autenticação)

#### Avaliações
- Listar avaliações: `GET /api/ratings/`
- Filtrar avaliações: `GET /api/ratings/?book_title=TITULO&book_authors=AUTOR`
- Criar avaliação: `POST /api/ratings/` (requer autenticação)

### Exportação de Dados

- Exportar livros: `GET /api/export/books/`
- Exportar avaliações: `GET /api/export/ratings/`

### Documentação Swagger

- Acesse a documentação no navegador: `http://127.0.0.1:8000/api/docs/`

---

## Testes Automatizados

Para executar os testes automatizados:

```bash
py manage.py test
```

---
