## **Como usar**:
O bot só funciona enquanto o processo inicial estiver rodando, para checar, verifique se o bot está online no servidor.  
Não se esqueça de baixar as bibliotecas utilizadas (pip install py-cord) / (pip install -r requirements.txt).  
Recomendo utilizar um ambiente virtual.  
Tente seguir o padrão pré estabelecido, se fugir muito escopo eu vou perseguir vocês  
-ZC
    
Eu recomendo rodar no linux ou no wsl se puder, já que algumas bibliotecas estão funcionando diferente em outros sistemas e estamos desenvolvendo
com foco para rodar em linux.  
-CJ

## **Requisitos**:
Recomentamos o uso de Python 3.8 para cima. As bibliotecas necessárias estão listadas em requirements.txt  

### Especiais:
Utilizamos a biblioteca `pdf2image` para transformar pdf em png, e ela precisa do _poppler_ instalado no sistema.  
Para instalar no linux é simples, apenas mande um `sudo apt-get install poppler-utils` no terminal. 
Para instalar em outros sistemas, verifique no [README do pdf2image](https://github.com/Belval/pdf2image#how-to-install).


É necessário ter instalado o _ffmpeg_ para conseguir reproduzir audios em canais de voz.  
Para instalar no linux, use `sudo apt-get install ffmpeg` no termial.  
Para windows, clique [aqui](https://ffmpeg.org/download.html#build-windows) e para MacOS, clique [aqui](https://ffmpeg.org/download.html#build-mac).  
Para windows, ffmpeg.exe deve estar na pasta do projeto (por enquanto)


## **Funcionalidades**:
- Implementar estrutura inicial. ZC ✅
- GetProvas. ZC ✅
- getResumos ZC ✅

- cadastrar datas de provas ZC

- Ler o PDF de ementa e separar as palavras chave em variáveis para usar em um embeed ZC
- Upgrade no getResumos e GetProvas -> Depende de local-files ZC

- Implementar funções por comando "/exemplo" CJ ✅
- getEmentaMateria (tal) CJ ✅
- getCurrentCalendario CJ
    - getCurrentCalendario text CJ
- Criar tratamento de Erros
- Infos

- getTurorial (software) (talvez) ADN

- canal de avisos (baseado nas provas) ADY

**Tarefas:**
- Criação de um arquivo PY com constantes de Links
- Release ceffy 1.0
- Fazer comando infos CJ ✅
- Criar ceffy dev ZC
- Ajustes finais ceffy prod CJ
- Verificar disponibilidade da ceffy em outros servers ZC
- Hospedar ceffy CJ
- Fazer comando EG CJ ✅
- Arrumar compatibilidade entre win/linux

