# ![Cycle DELF](https://img.shields.io/badge/🇫🇷%20Cycle%20DELF-Préparation%204x15-blue?style=for-the-badge&labelColor=white&color=red)

**Desenvolvido por Giovana Santiago Lima** *Trabalho Prático de Banco de Dados NoSQL — Sistemas de Informação / Gestão da Informação (UFU)*

---

## 📘 Visão Geral
O **Cycle DELF** é uma plataforma inteligente projetada para estudantes que buscam a certificação francesa (B1/B2). O sistema utiliza a metodologia **4×15** — 1 hora diária dividida em 4 blocos de 15 minutos — garantindo equilíbrio entre as competências do exame sem sobrecarga mental.

O diferencial técnico deste projeto é a arquitetura de **Persistência Poliglota**, utilizando três modelos NoSQL distintos para resolver desafios específicos de performance, conexão e busca semântica.



---

## 🛠️ Arquitetura de Dados (NoSQL)

A escolha das tecnologias foi baseada na natureza de cada dado do ecossistema:

### 1. ⚡ Redis (Key-Value)
Focado em **Alta Performance** e métricas em tempo real.
* **Streak Tracker (Bitmaps):** Gerencia a constância do usuário com baixíssimo consumo de memória.
* **Vocabulário (HyperLogLog):** Contagem eficiente de termos únicos encontrados pelo aluno durante os estudos.

### 2. 🕸️ Neo4j (Grafos)
Focado em **Relacionamento e Descoberta**.
* **Knowledge Graph:** Mapeamento de conexões entre `Usuarios` e `Materiais`.
* **Recomendação:** Identificação de "materiais hubs" e perfis de estudo similares através de relacionamentos `ESTUDOU`.



### 3. 🍃 MongoDB Atlas (Documento & Vetor)
Focado em **Flexibilidade e IA**.
* **Base Documental:** Armazenamento central de todos os materiais de estudo.
* **Vector Search (Busca Semântica):** Implementação de busca por significado utilizando Embeddings (`paraphrase-multilingual-MiniLM-L12-v2`). O sistema encontra conteúdos por contexto, indo além da simples busca por palavras-chave.



---

## ✨ Funcionalidades Principais

* **Busca Inteligente:** Encontre materiais por intenção (ex: buscar "comida" retorna "déjeuner" ou "gastronomie").
* **Visualização de Grafo:** Interface que mostra como o conhecimento está distribuído entre os usuários.
* **Gamificação:** Streak diário que incentiva o hábito sem pesar no carregamento da página.
* **Gerador 4×15:** Organização automática das competências: *Compréhension Orale, Production Écrite, Compréhension Écrite e Production Orale.*

---

## 🚀 Stack Tecnológica

* **Linguagem:** Python 3.12 (FastAPI)
* **Modelos de IA:** Sentence-Transformers (HuggingFace)
* **Bancos de Dados:** MongoDB Atlas, Redis Cloud, Neo4j Aura
* **Front-end:** Streamlit /  JS

---

## 📂 Estrutura do Projeto

* `/app`: Código-fonte da API, rotas e integração com bancos.
* `/screenshots`: Evidências de funcionamento (Busca Vetorial, Grafos e Redis).
* `vetor.py`: Script para extração e povoamento de embeddings no MongoDB.
* `grafo.py`: Script para modelagem e criação de relacionamentos no Neo4j.

