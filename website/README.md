# Documentação do Field War

Site feito com [Docusaurus](https://docusaurus.io/) 3. Coloque esta pasta (`website/`) na raiz do repositório `Field_War`.

```bash
cd website
npm install
npm start        # http://localhost:3000/Field_War/
npm run build    # gera a pasta build/
```

Requer Node.js 20 ou superior.

## Publicar no GitHub Pages

O `docusaurus.config.js` já usa `url: https://matheusrooliveira.github.io` e `baseUrl: /Field_War/`.
Se o repositório for de outra conta ou tiver outro nome, ajuste `url`, `baseUrl`, `organizationName` e `projectName`.

```bash
GIT_USER=<seu-usuario-github> npm run deploy
```
