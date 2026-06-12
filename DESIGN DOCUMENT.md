# Software Design Document (SDD)
## Sistema de Doações — MVP

**Versão:** 1.0  
**Data:** Junho 2026  
**Equipa:** Equipa de Desenvolvimento  
**Estado:** Rascunho

---

## 1. Introdução

### 1.1 Objectivo

Este documento descreve o design do sistema de doações, cobrindo os requisitos funcionais, módulos, actores e decisões de arquitectura para o MVP.

### 1.2 Âmbito

O sistema permite que doadores encontrem centros de doação, registem doações e acompanhem o histórico. Os centros gerem campanhas, confirmam recepções e controlam stock. A equipa de desenvolvimento (admin) supervisiona toda a plataforma.

### 1.3 Definições e Siglas

| Termo | Descrição |
|-------|-----------|
| MVP | Minimum Viable Product |
| RF | Requisito Funcional |
| SDD | Software Design Document |
| Admin | Equipa interna de desenvolvimento com acesso total à plataforma |

---

## 2. Actores do Sistema

| Actor | Descrição |
|-------|-----------|
| **Doador** | Utilizador que regista conta e efectua doações |
| **Centro de Doação** | Organização registada que recebe e gere doações |
| **Admin** | Equipa de desenvolvimento com acesso total à plataforma |

---

## 3. Requisitos Funcionais

### 3.1 Módulo Doador

| ID | Requisito | Prioridade |
|----|-----------|-----------|
| RF-D01 | Registar conta com nome, email, senha e localização | Alta |
| RF-D02 | Fazer login e recuperar senha por email | Alta |
| RF-D03 | Listar centros de doação próximos com endereço e contacto | Alta |
| RF-D04 | Registar uma doação (tipo, quantidade, data) e consultar histórico | Alta |
| RF-D05 | Receber notificações de campanhas activas e confirmações | Média |

### 3.2 Módulo Centro de Doação

| ID | Requisito | Prioridade |
|----|-----------|-----------|
| RF-C01 | Registar e gerir o perfil do centro (nome, endereço, contacto, horário) | Alta |
| RF-C02 | Publicar campanhas de doação com tipo, meta e prazo | Alta |
| RF-C03 | Confirmar e registar recepção de doações dos doadores | Alta |
| RF-C04 | Consultar histórico de doações recebidas com filtros básicos | Alta |
| RF-C05 | Gerir stock de doações disponíveis (entrada, saída, saldo) | Média |

### 3.3 Módulo Admin

| ID | Requisito | Prioridade |
|----|-----------|-----------|
| RF-A01 | Aprovar ou rejeitar o registo de centros de doação | Alta |
| RF-A02 | Gerir utilizadores (suspender, reativar, eliminar contas) | Alta |
| RF-A03 | Monitorizar doações e actividade geral da plataforma | Alta |
| RF-A04 | Enviar comunicados e notificações globais a doadores e centros | Média |
| RF-A05 | Consultar relatórios e métricas básicas (total de doações, centros activos) | Média |

---

## 4. Requisitos Não Funcionais (MVP)

| Categoria | Requisito |
|-----------|-----------|
| **Segurança** | Senhas encriptadas (bcrypt); autenticação via JWT |
| **Disponibilidade** | Sistema disponível 99% do tempo em horário útil |
| **Usabilidade** | Interface responsiva acessível em mobile e desktop |
| **Performance** | Respostas da API em menos de 2 segundos para operações comuns |
| **Escalabilidade** | Arquitectura que suporte crescimento horizontal no futuro |

---

## 5. Arquitectura do Sistema

### 5.1 Visão Geral

O MVP segue uma arquitectura de três camadas:

```
[ Cliente Web / Mobile ]
         |
[ API REST (Backend) ]
         |
[ Base de Dados Relacional ]
```

### 5.2 Tecnologias Sugeridas

| Camada | Tecnologia |
|--------|-----------|
| Frontend | React / React Native |
| Backend | Node.js + Express (ou NestJS) |
| Base de Dados | PostgreSQL |
| Autenticação | JWT + bcrypt |
| Notificações | Firebase Cloud Messaging (FCM) |
| Hosting | AWS / GCP / Railway |

---

## 6. Modelo de Dados (Esboço)

### 6.1 Entidades Principais

**users**
- `id`, `name`, `email`, `password_hash`, `location`, `role` (donor / center / admin), `status`, `created_at`

**donation_centers**
- `id`, `user_id` (FK), `name`, `address`, `phone`, `schedule`, `status` (pending / approved / rejected), `created_at`

**campaigns**
- `id`, `center_id` (FK), `title`, `donation_type`, `goal`, `deadline`, `status`, `created_at`

**donations**
- `id`, `donor_id` (FK), `center_id` (FK), `campaign_id` (FK, nullable), `type`, `quantity`, `date`, `status` (pending / confirmed), `created_at`

**stock**
- `id`, `center_id` (FK), `donation_type`, `quantity`, `updated_at`

**notifications**
- `id`, `user_id` (FK), `title`, `body`, `read`, `created_at`

---

## 7. Fluxos Principais

### 7.1 Registo e Login

1. Doador ou centro preenche o formulário de registo
2. Sistema envia email de confirmação
3. No caso de centro, o admin aprova o registo (RF-A01)
4. Utilizador faz login e recebe token JWT

### 7.2 Doação

1. Doador consulta centros e campanhas próximas (RF-D03)
2. Doador regista a doação com tipo, quantidade e data (RF-D04)
3. Doação fica com status `pending`
4. Centro confirma a recepção (RF-C03), status muda para `confirmed`
5. Stock do centro é actualizado automaticamente (RF-C05)
6. Doador recebe notificação de confirmação (RF-D05)

### 7.3 Gestão de Campanha

1. Centro publica campanha com tipo, meta e prazo (RF-C02)
2. Sistema notifica doadores da área (RF-D05)
3. Doações entram com referência à campanha
4. Centro acompanha progresso via histórico (RF-C04)

---

## 8. Pontos em Aberto

Os itens abaixo devem ser decididos antes de iniciar o desenvolvimento:

| # | Questão | Impacto |
|---|---------|---------|
| 1 | Tipos de doação suportados (sangue, bens materiais, ou ambos)? | Modelo de dados e formulários |
| 2 | A confirmação pelo centro é obrigatória para validar a doação? | Fluxo de doação e estatísticas |
| 3 | Aprovação de centros é manual ou automática (ex: via NIF)? | Módulo admin e UX do centro |

---

## 9. Fora do Âmbito do MVP

- Pagamentos ou doações monetárias
- Integração com sistemas externos (ex: hospitais, Ministério da Saúde)
- App nativa (iOS/Android) — o MVP usa web responsiva
- Sistema de avaliações ou reputação de centros
- Relatórios avançados ou exportação de dados

---

*Documento gerado em Junho de 2026 — sujeito a revisão após alinhamento dos pontos em aberto.*