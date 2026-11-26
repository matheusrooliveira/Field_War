// @ts-check
import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Field War',
  tagline: 'One mission. One battlefield. No second chances.',
  favicon: 'img/nave.png',

  // Ajuste conforme o local de publicação (GitHub Pages do repositório).
  url: 'https://matheusrooliveira.github.io',
  baseUrl: '/Field_War/',
  organizationName: 'matheusrooliveira',
  projectName: 'Field_War',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  i18n: {
    defaultLocale: 'pt-BR',
    locales: ['pt-BR'],
  },

  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          routeBasePath: 'docs',
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/matheusrooliveira/Field_War/tree/main/website/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/banner-fieldwar.png',
      colorMode: {
        defaultMode: 'dark',
        disableSwitch: false,
        respectPrefersColorScheme: false,
      },
      navbar: {
        title: 'FIELD WAR',
        logo: {alt: 'Nave do Field War', src: 'img/nave.png'},
        items: [
          {type: 'docSidebar', sidebarId: 'docs', position: 'left', label: 'Documentação'},
          {to: '/docs/arquitetura/diagramas', label: 'Diagramas', position: 'left'},
          {to: '/docs/banco-de-dados', label: 'Banco de dados', position: 'left'},
          {
            href: 'https://github.com/matheusrooliveira/Field_War',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Documentação',
            items: [
              {label: 'Visão geral', to: '/docs/intro'},
              {label: 'Como executar', to: '/docs/como-executar'},
              {label: 'Jogabilidade', to: '/docs/jogabilidade/controles'},
            ],
          },
          {
            title: 'Projeto',
            items: [
              {label: 'Arquitetura', to: '/docs/arquitetura/estrutura'},
              {label: 'GitHub', href: 'https://github.com/matheusrooliveira/Field_War'},
            ],
          },
        ],
        copyright: `Field War — projeto acadêmico de Ciência da Computação. Documentação feita com Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'sql', 'bash'],
      },
      mermaid: {
        theme: {light: 'neutral', dark: 'dark'},
      },
    }),
};

export default config;
