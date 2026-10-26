import type {ReactNode} from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import CodeBlock from '@theme/CodeBlock';
import useBaseUrl from '@docusaurus/useBaseUrl';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
// Written by tools/gen_docs.py on every build, with a drawing of each sport's surface under static/img/home/:
// the version, the install line and the sports (a new sport appears here without an edit).
import home from '@site/src/data/home.json';
import styles from './index.module.css';

type FeatureItem = {
  title: string;
  to: string;
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Rule-book dimensions',
    to: '/docs/reference/',
    description: (
      <>
        A class per league, drawn to the dimensions in that league&apos;s rule book: the NHL,
        NFL, NBA, MLB, FIFA, the PLL and dozens more.
      </>
    ),
  },
  {
    title: 'Plot your data on it',
    to: '/docs/reference/plotting',
    description: (
      <>
        <code>scatter</code>, <code>heatmap</code>, <code>contour</code>, <code>hexbin</code> and{' '}
        <code>arrow</code> on the surface&apos;s own coordinates, kept inside its boundaries.
      </>
    ),
  },
  {
    title: 'Any units, any view',
    to: '/docs/getting-started',
    description: (
      <>
        Draw in the league&apos;s units or any other, rotate to a TV or a vertical view, and show
        the whole surface or just the part you need: an offensive half, a red zone, a house.
      </>
    ),
  },
  {
    title: 'Your colors',
    to: '/docs/getting-started',
    description: (
      <>
        <code>update_colors()</code> restyles every feature, and <code>update_*_params()</code>{' '}
        redraws a surface for a league sportypy doesn&apos;t ship yet.
      </>
    ),
  },
  {
    title: 'Parity with sportyR',
    to: 'https://sportyR.sportsdataverse.org',
    description: (
      <>
        The same leagues, dimensions and colors as{' '}
        <Link to="https://sportyR.sportsdataverse.org">sportyR</Link>, checked point for point
        against what sportyR draws.
      </>
    ),
  },
  {
    title: 'Part of the SportsDataverse',
    to: 'https://sportsdataverse.org',
    description: (
      <>
        Pairs with <Link to="https://sdvplot.sportsdataverse.org">sdvplot</Link> for team logos and
        colors, and with <Link to="https://py.sportsdataverse.org">sdv-py</Link> for the
        play-by-play to put on the surface.
      </>
    ),
  },
];

const SAMPLE = `import matplotlib.pyplot as plt
from sportypy.surfaces.hockey import NHLRink

nhl = NHLRink()
ax = nhl.draw(display_range = "offense")
nhl.scatter([80, 70, 85], [10, -15, 3], ax = ax, color = "#e06000")
plt.show()`;

// A card per blurb; the title is the link, so the description can still hold links of its own.
function Feature({title, to, description}: FeatureItem): ReactNode {
  return (
    <div className={clsx('col col--4', styles.feature)}>
      <div className={clsx('card', styles.card)}>
        <h3 className={styles.cardTitle}>
          <Link to={to}>{title}</Link>
        </h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

function HomepageHeader(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <img className={styles.heroLogo} src={useBaseUrl('/img/logo.png')} alt="" width={120} height={125} />
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link className="button button--secondary button--lg" to="/docs/intro">
            Get started
          </Link>
          <Link className="button button--outline button--secondary button--lg" to="/docs/reference/">
            API reference
          </Link>
        </div>
        <p className={styles.version}>Version {home.version}</p>
      </div>
    </header>
  );
}

function TryIt(): ReactNode {
  return (
    <section className={styles.section}>
      <div className="container">
        <h2>Install and try it</h2>
        <CodeBlock language="bash">{home.install}</CodeBlock>
        <CodeBlock language="python">{SAMPLE}</CodeBlock>
        <p>
          <Link to="/docs/getting-started">The usage guide</Link> covers display ranges, units,
          rotation and colors.
        </p>
      </div>
    </section>
  );
}

// Each sport's surface as sportypy draws it (tools/gen_docs.py renders them at build time)
function Surfaces(): ReactNode {
  const imageUrl = useBaseUrl('/img/home/');
  return (
    <section className={styles.section}>
      <div className="container">
        <h2>Every surface, to scale</h2>
        <ul className={styles.surfaces}>
          {home.sports.map((s) => (
            <li key={s.sport} className={styles.surface}>
              <Link to={`/docs/reference/surfaces/${s.sport}`} className={styles.surfaceLink}>
                <img
                  src={`${imageUrl}${s.sport}.png`}
                  alt={`A ${s.title.toLowerCase()} surface (${s.example}) drawn by sportypy`}
                  loading="lazy"
                />
                <span className={styles.surfaceName}>{s.title}</span>
                <span className={styles.surfaceMeta}>
                  <code>{s.base}</code> · {s.leagues} league{s.leagues === 1 ? '' : 's'}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout title={siteConfig.title} description={siteConfig.tagline}>
      <HomepageHeader />
      <main>
        <TryIt />
        <Surfaces />
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              {FeatureList.map((props) => (
                <Feature key={props.title} {...props} />
              ))}
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
