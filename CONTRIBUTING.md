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
git add .
git commit -m "Mensagem do commit"
```

### 7. 📢 Push para o repositório remoto

```bash
git push origin nome-usuario-minha-funcionalidade
```

### 8. 📢 Solicite a revisão do seu branch

```bash
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

