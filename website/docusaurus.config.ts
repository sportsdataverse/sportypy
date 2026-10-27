import type {PrismTheme} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// The sportypy docs site. It follows the SportsDataverse docs family (sdvplot, sdv-py, sdvplot-js): the same
// structure, navbar, footer and shared stylesheet (src/css/sdv-theme.css, byte-identical to sdvplot's), in
// sportypy's own colors and type (src/css/custom.css): the logo's greens, sportyR's orange, Roboto.
//
// Everything under docs/reference/, docs/getting-started.md, src/pages/CHANGELOG.md, src/data/home.json and
// static/img/home/ is written by tools/gen_docs.py from the docstrings, the README and CHANGELOG.md. The
// prestart and prebuild scripts run it, so `yarn start` and `yarn build` always show the current code; none of
// it is committed. Only intro.md, the homepage and the theme files are hand-written.

const PLAUSIBLE_ID = 'pa-lI8N5cCc-JaTGLO7Mhsgb'; // Plausible site sportypy.sportsdataverse.org ('' disables analytics)
const analytics = PLAUSIBLE_ID
  ? {
      scripts: [{src: `https://plausible.io/js/${PLAUSIBLE_ID}.js`, async: true}],
      headTags: [{tagName: 'script', attributes: {}, innerHTML:
        'window.plausible=window.plausible||function(){(plausible.q=plausible.q||[]).push(arguments)},plausible.init=plausible.init||function(i){plausible.o=i||{}};plausible.init()'}],
    }
  : {scripts: [], headTags: []};

// Code-block themes in the sportypy palette. Every token clears 4.5:1 on its surface.
const sportyPrismLight: PrismTheme = {
  plain: {color: '#1b1611', backgroundColor: '#ffffff'},
  styles: [
    {types: ['comment', 'prolog', 'doctype', 'cdata'], style: {color: '#57524a', fontStyle: 'italic'}},
    {types: ['punctuation', 'operator'], style: {color: '#57524a'}},
    {types: ['keyword', 'tag', 'selector', 'atrule', 'important'], style: {color: '#006838'}},
    {types: ['string', 'char', 'attr-value', 'regex', 'inserted', 'triple-quoted-string', 'url'], style: {color: '#a34400'}},
    {types: ['number', 'boolean', 'constant', 'symbol', 'deleted'], style: {color: '#9b1c5a'}},
    {types: ['function', 'class-name', 'decorator', 'annotation'], style: {color: '#1d4f91'}},
  ],
};

const sportyPrismDark: PrismTheme = {
  plain: {color: '#e8efea', backgroundColor: '#13221a'},
  styles: [
    {types: ['comment', 'prolog', 'doctype', 'cdata'], style: {color: '#9fb0a4', fontStyle: 'italic'}},
    {types: ['punctuation', 'operator'], style: {color: '#9fb0a4'}},
    {types: ['keyword', 'tag', 'selector', 'atrule', 'important'], style: {color: '#3cc456'}},
    {types: ['string', 'char', 'attr-value', 'regex', 'inserted', 'triple-quoted-string', 'url'], style: {color: '#ff8a3d'}},
    {types: ['number', 'boolean', 'constant', 'symbol', 'deleted'], style: {color: '#f28bc0'}},
    {types: ['function', 'class-name', 'decorator', 'annotation'], style: {color: '#8cc3ff'}},
  ],
};

const config: Config = {
  future: {
    v4: true,
    faster: true,
  },
  title: 'sportypy',
  tagline: 'Regulation, to-scale sports surfaces for matplotlib: the Python counterpart of sportyR.',
  url: 'https://sportypy.sportsdataverse.org',
  baseUrl: '/',
  // Fails the build on a broken link: fix a generated page in tools/gen_docs.py or the docstring, never by hand
  onBrokenLinks: 'throw',
  favicon: 'img/favicon.png',
  organizationName: 'sportsdataverse',
  projectName: 'sportypy',
  i18n: {defaultLocale: 'en', locales: ['en']},
  // .md pages (the generated reference) are CommonMark, so braces and angle brackets in docstrings and
  // signatures need no MDX escaping; .mdx pages keep MDX
  markdown: {
    format: 'detect',
    hooks: {onBrokenMarkdownLinks: 'throw'},
  },
  scripts: analytics.scripts,
  headTags: analytics.headTags,
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Generated pages have no edit link: they are fixed in the docstrings (or the README / changelog)
          editUrl: ({docPath}) =>
            /^reference\/|^getting-started\.md$/.test(docPath)
              ? undefined
              : `https://github.com/sportsdataverse/sportypy/edit/main/website/docs/${docPath}`,
        },
        // No blog: release notes live on the News page (the changelog)
        blog: false,
        theme: {
          // The shared family theme first, then sportypy's colors, type and site rules
          customCss: [
            require.resolve('@fontsource-variable/roboto'),
            require.resolve('@fontsource-variable/roboto-condensed'),
            require.resolve('@fontsource-variable/roboto-mono'),
            './src/css/sdv-theme.css',
            './src/css/custom.css',
          ],
        },
      } satisfies Preset.Options,
    ],
  ],
  // Offline full-text search: the index is built into the static output at build time
  themes: [
    [
      '@easyops-cn/docusaurus-search-local',
      {hashed: true, indexBlog: false},
    ],
  ],
  themeConfig: {
    docs: {
      sidebar: {hideable: true},
    },
    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    image: 'img/social-card.png',
    metadata: [
      {property: 'og:type', content: 'website'},
      {property: 'og:site_name', content: 'sportypy | SportsDataverse'},
      {property: 'og:image:alt', content: 'sportypy'},
      {name: 'twitter:site', content: '@sportsdataverse'},
      {name: 'twitter:image:alt', content: 'sportypy'},
    ],
    navbar: {
      hideOnScroll: true,
      // The logo's deep green in both color modes; custom.css sets the colors
      style: 'dark',
      title: 'sportypy',
      logo: {alt: 'sportypy logo', src: 'img/logo.png'},
      items: [
        {type: 'doc', docId: 'intro', position: 'left', label: 'Docs'},
        {label: 'News', to: 'CHANGELOG', position: 'left'},
        // SportsDataverse package directory, as on the other family sites. Sourced from
        //   https://sportsdataverse.org/packages
        //   https://github.com/sportsdataverse/.github/blob/main/profile/README.md
        // Keep it in sync with sdvplot's docusaurus.config.ts. `sdv-packages-dropdown` turns on the
        // multi-column mega-menu in sdv-theme.css.
        {
          label: 'SDV',
          position: 'left',
          className: 'sdv-packages-dropdown',
          items: [
            {href: 'https://sportsdataverse.org', label: 'SportsDataverse', target: '_self', className: 'sdv-section-header'},
            {href: 'https://sportsdataverse.org/cheatsheets/sportypy.pdf', label: 'Cheat Sheet (PDF)', target: '_self'},
            {href: 'https://sportsdataverse.org/cheatsheets', label: 'All Cheat Sheets', target: '_self'},
            // -- Python --
            {label: 'Python Packages', href: 'https://py.sportsdataverse.org/', target: '_self', className: 'sdv-section-header'},
            {label: 'sportsdataverse-py', href: 'https://py.sportsdataverse.org/', target: '_self'},
            {label: 'sdvplot', href: 'https://sdvplot.sportsdataverse.org/', target: '_self'},
            {label: 'sportypy', href: 'https://sportypy.sportsdataverse.org/', target: '_self'},
            {label: 'collegebaseball', href: 'https://collegebaseball.readthedocs.io/en/latest/index.html', target: '_self'},
            {label: 'nwslpy', href: 'https://github.com/nwslR/nwslpy', target: '_self'},
            // -- R --
            {label: 'R Packages', href: 'https://r.sportsdataverse.org/', className: 'sdv-section-header'},
            {label: 'sportsdataverse-R', href: 'https://r.sportsdataverse.org/', target: '_self'},
            {label: 'sdvplotR', href: 'https://sdvplotR.sportsdataverse.org/', target: '_self'},
            {label: 'cfbfastR', href: 'https://cfbfastR.sportsdataverse.org/', target: '_self'},
            {label: 'hoopR', href: 'https://hoopR.sportsdataverse.org/', target: '_self'},
            {label: 'wehoop', href: 'https://wehoop.sportsdataverse.org/', target: '_self'},
            {label: 'fastRhockey', href: 'https://fastRhockey.sportsdataverse.org/', target: '_self'},
            {label: 'baseballr', href: 'https://BillPetti.github.io/baseballr/', target: '_self'},
            {label: 'sportyR', href: 'https://sportyR.sportsdataverse.org/', target: '_self'},
            {label: 'ggshakeR', href: 'https://abhiamishra.github.io/ggshakeR/', target: '_self'},
            {label: 'soccerAnimate', href: 'https://github.com/Dato-Futbol/soccerAnimate', target: '_self'},
            {label: 'oddsapiR', href: 'https://oddsapiR.sportsdataverse.org/', target: '_self'},
            {label: 'mlbplotR', href: 'https://camdenk.github.io/mlbplotR/', target: '_self'},
            {label: 'cfbplotR', href: 'https://cfbplotR.sportsdataverse.org/', target: '_self'},
            {label: 'cfb4th', href: 'https://cfb4th.sportsdataverse.org/', target: '_self'},
            {label: 'cfbseedR', href: 'https://cfbseedR.sportsdataverse.org/', target: '_self'},
            {label: 'softballR', href: 'https://github.com/sportsdataverse/softballR/', target: '_self'},
            {label: 'nwslR', href: 'https://github.com/nwslR/nwslR/', target: '_self'},
            {label: 'usfootballR', href: 'https://usfootballR.sportsdataverse.org/', target: '_self'},
            {label: 'recruitR', href: 'https://recruitR.sportsdataverse.org/', target: '_self'},
            {label: 'puntr', href: 'https://puntalytics.github.io/puntr/', target: '_self'},
            {label: 'chessR', href: 'https://jaseziv.github.io/chessR/', target: '_self'},
            // -- Node.js --
            {label: 'Node.js Packages', href: 'https://js.sportsdataverse.org/', className: 'sdv-section-header'},
            {label: 'sportsdataverse.js', href: 'https://js.sportsdataverse.org/', target: '_self'},
            {label: 'sdvplot-js', href: 'https://plot.sportsdataverse.org/', target: '_self'},
            {label: 'nfl-nerd', href: 'https://github.com/nntrn/nfl-nerd/', target: '_self'},
          ],
        },
        {label: 'sportyR', href: 'https://sportyR.sportsdataverse.org/', position: 'right'},
        {label: 'GitHub', href: 'https://github.com/sportsdataverse/sportypy', position: 'right'},
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {label: 'Get started', to: '/docs/intro'},
            {label: 'Usage guide', to: '/docs/getting-started'},
            {label: 'Cookbooks', to: '/docs/cookbooks'},
            {label: 'API reference', to: '/docs/reference/'},
            {label: 'Plotting and display', to: '/docs/reference/plotting'},
            {label: 'News', to: '/CHANGELOG'},
          ],
        },
        {
          title: 'Community',
          items: [
            {label: 'GitHub', href: 'https://github.com/sportsdataverse/sportypy'},
            {label: 'Issues', href: 'https://github.com/sportsdataverse/sportypy/issues'},
            {label: 'Bluesky', href: 'https://bsky.app/profile/sportsdataverse.org'},
            {label: 'X', href: 'https://x.com/SportsDataverse'},
          ],
        },
        {
          title: 'SportsDataverse',
          items: [
            {label: 'sportsdataverse.org', href: 'https://sportsdataverse.org'},
            {label: 'sportyR', href: 'https://sportyR.sportsdataverse.org'},
            {label: 'sdvplot', href: 'https://sdvplot.sportsdataverse.org'},
            {label: '@sportsdataverse/sporty (JS)', href: 'https://plot.sportsdataverse.org'},
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} <strong>sportypy</strong>, developed by <a href='https://github.com/rossdrucker'>Ross Drucker</a>, part of the <a href='https://sportsdataverse.org'>SportsDataverse</a>. Released under the GPL-3.0 license.`,
    },
    prism: {
      theme: sportyPrismLight,
      darkTheme: sportyPrismDark,
      additionalLanguages: ['bash'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
