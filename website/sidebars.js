// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docs: [
    'intro',
    'como-executar',
    {
      type: 'category',
      label: 'Jogabilidade',
      collapsed: false,
      items: [
        'jogabilidade/controles',
        'jogabilidade/regras',
        'jogabilidade/powerups',
        'jogabilidade/boss',
      ],
    },
    {
      type: 'category',
      label: 'Arquitetura',
      collapsed: false,
      items: [
        'arquitetura/estrutura',
        'arquitetura/modulos',
        'arquitetura/ciclo-do-jogo',
        'arquitetura/diagramas',
      ],
    },
    'banco-de-dados',
    'audio',
    'tecnologias',
    'melhorias-futuras',
  ],
};

export default sidebars;
