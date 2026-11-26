import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import Layout from '@theme/Layout';
import styles from './index.module.css';

const destaques = [
  {
    titulo: 'Combate arcade',
    texto: 'Pilote a nave, destrua ondas de inimigos e colete power-ups em sessões de cinco minutos.',
    link: '/docs/jogabilidade/regras',
  },
  {
    titulo: 'Boss em 3 fases',
    texto: 'Um chefe com atração magnética, escudos orbitais e ataques cada vez mais rápidos.',
    link: '/docs/jogabilidade/boss',
  },
  {
    titulo: 'Ranking com SQLite',
    texto: 'Login do jogador, recordes salvos em banco de dados e Top 10 no menu.',
    link: '/docs/banco-de-dados',
  },
  {
    titulo: 'Arquitetura e UML',
    texto: 'Módulos, ciclo do jogo e diagramas de classe, herança e sequência.',
    link: '/docs/arquitetura/diagramas',
  },
];

export default function Home() {
  const banner = useBaseUrl('/img/banner-fieldwar.png');

  return (
    <Layout
      title="Documentação"
      description="Documentação do Field War, um shooter espacial 2D em Python e Pygame.">
      <header className={clsx('hero', styles.hero)}>
        <div className="container">
          <img className={styles.banner} src={banner} alt="Banner do Field War" />
          <h1 className={styles.titulo}>FIELD WAR</h1>
          <p className={styles.tagline}>Shooter espacial 2D feito em Python e Pygame</p>
          <div className={styles.botoes}>
            <Link className="button button--primary button--lg" to="/docs/intro">
              Ler a documentação
            </Link>
            <Link className="button button--outline button--primary button--lg" to="/docs/como-executar">
              Como executar
            </Link>
          </div>
        </div>
      </header>
      <main className="container margin-vert--xl">
        <div className="row">
          {destaques.map((d) => (
            <div key={d.titulo} className="col col--3 margin-bottom--lg">
              <Link to={d.link} className={styles.card}>
                <h3>{d.titulo}</h3>
                <p>{d.texto}</p>
              </Link>
            </div>
          ))}
        </div>
      </main>
    </Layout>
  );
}
