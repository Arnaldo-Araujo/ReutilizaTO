# Projeto Integrador – 3º Período

## 🎯 Tema

**Sistema de Troca e Doação de Produtos Comunitários**

## 📖 Descrição Geral

Desenvolvimento de um **sistema web** para facilitar a **troca e/ou doação de produtos** em comunidades do interior do Tocantins, promovendo a economia colaborativa e o reaproveitamento de bens como:

- Roupas
- Móveis
- Eletrodomésticos
- Materiais escolares

Usuários principais:

- Moradores
- ONGs
- Associações comunitárias

Funcionalidades como: cadastro de produtos, busca por itens, registro de trocas ou doações, e direcionamento de doações a famílias ou instituições.

## 🧠 Disciplinas Envolvidas

- Engenharia de Requisitos  
- Banco de Dados I  
- Programação para Web I  
- Sistemas Operacionais  
- Redes de Computadores I  

---

## 📌 Funcionalidades do Sistema

- **Cadastro de Usuários**  
  Registro de perfil com dados básicos e preferências.

- **Cadastro de Produtos**  
  Informações como fotos, descrição, categoria, condição (novo/usado) e status (disponível/reservado/doado).

- **Busca e Filtro**  
  Busca com filtros por categoria, localização e tipo de transação (troca/doação).

- **Troca e/ou Doação**  
  Comunicação entre usuários e registro das transações no banco de dados.

---

## 🧾 Objetivos por Disciplina

### 📘 Engenharia de Requisitos

- Identificar problema e propósitos do sistema
- Levantar requisitos com usuários
- Identificar requisitos funcionais e não funcionais
- Modelagem BPMN
- Documento de Requisitos

### 🧮 Banco de Dados I

- Diagrama Entidade-Relacionamento
- Texto explicativo da lógica do negócio
- Criação do banco relacional
- Garantir integridade com PKs e FKs
- Consultas SQL

### 🌐 Redes de Computadores

- Configurar servidor web
- Definir IP e máscara
- Garantir acesso ao sistema na máquina virtual

### 🖥 Sistemas Operacionais

- Configurar máquina virtual com Linux ou Windows
- Gerenciar permissões
- Criar imagem do ambiente

### 💻 Programação para Web I

- Protótipo front-end + back-end
- Implementar pelo menos 4 funcionalidades CRUD
- Entrega individual via GitHub

---

## 📅 Cronograma e Entregas

| Entrega                             | Peso | Data     |
|------------------------------------|------|----------|
| Formação dos grupos                | —    | 17/03    |
| Documento de Requisitos + BPMN     | 1,0  | 08/05    |
| Modelagem + Modelo Físico do BD    | 1,0  | 12/05    |
| Configuração do SO / Servidor (VM) | 1,0  | 15/05    |
| Protótipo (Front-end, Back-end)    | 1,0  | 05/04, 24/04, 22/05 |
| Apresentação Final                 | 2,0  | 29/05    |

---

## 📝 Critérios de Avaliação

- **Total: 6,0 pontos**
- Apresentação oral: **2,0 pontos**
- Entregas técnicas: **4,0 pontos**
- Avaliação individual (código via GitHub)
- Máquina virtual configurada e funcionando

---

## 📋 Requisitos do Grupo

- Grupos de **3 a 5 estudantes**
- Grupos definidos até **17/03**
- Alunos sem grupo serão alocados por tutores

---

## 🎤 Apresentação Final

- Duração: **15 minutos**
- Apresentação das funcionalidades, organização do grupo e entregas individuais

---

## ✅ O que será entregue

- Documento de Requisitos + BPMN
- Modelagem do Banco de Dados
- Máquina Virtual (SO e servidor configurado)
- Protótipo (Front + Back-end)
- Código no GitHub
- Apresentação final em grupo

## 🤝 Como contribuir para o ReutilizaTO (via Terminal)

### 1. 🍴 Faça o Fork do Repositório

Atenção: o fork é feito **pelo site do GitHub**. Vá até:  
🔗 https://github.com/Arnaldo-Araujo/ReutilizaTO.git  
E clique no botão **"Fork"** no canto superior direito.

> Não é possível fazer fork direto via terminal, é necessário usar o site.

---

### 2. ⬇️ Clone o Fork para sua máquina

```bash
git clone https://github.com/SEU_USUARIO/ReutilizaTO.git
cd ReutilizaTO
```

### 3. 🔄 Configure o repositório original como remoto "upstream"
```bash
Copiar
Editar
git remote add upstream https://github.com/Arnaldo-Araujo/ReutilizaTO.git
```
### 4. 🔧 Crie um branch com seu nome ou tarefa

```bash
git checkout -b nome-usuario-minha-funcionalidade
exemplo: 
git checkout -b joao-cadastro-usuario
```
### 5. ✍️ Faça suas alterações no código
Edite os arquivos desejados, como README.md, index.html, pasta DocumentosDiversos/conteudo, etc.

### 6. 💾 Adicione e faça o commit das alterações

```bash
Copiar
Editar
git add .
git commit -m "Mensagem do commit"
```

### 7. 📢 Push para o repositório remoto

```bash
Copiar
Editar
git push origin nome-usuario-minha-funcionalidade
```

### 8. 📢 Solicite a revisão do seu branch

```bash
Copiar
Editar
git pull upstream master
```

### 9. 📢 Solicite a revisão do seu branch

```bash
git add .
git commit -m "feat: adiciona cadastro de usuário com validação"
```
### 7. ⬆️ Envie seu branch para o seu fork no GitHub

```bash
git push origin nome-usuario-minha-funcionalidade
```	

### 8. 🔁 Crie um Pull Request

Após o push, vá até seu fork no GitHub e clique em:

"Compare & Pull Request" → adicione um título e descrição → Create Pull Request

### 9. 🔄 Sincronize seu fork com atualizações do projeto original (opcional)

```bash
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

### 10. 📢 Solicite a revisão do seu branch

```bash
git add .
git commit -m "feat: adiciona cadastro de usuário com validação"
```

