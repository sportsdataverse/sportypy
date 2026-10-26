import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// A prototype of the sportypy site on Docusaurus, beside the Sphinx site in
// docs/ (which still builds and deploys). docs/reference/ and docs/changelog.md
// are written by tools/gen_docs.py from the docstrings and docs/changelog.md;
// the other pages are hand-written.
const config: Config = {
  future: {
    v4: true,
    faster: true,
  },
  title: 'sportypy',
  tagline: 'Regulation sports surfaces for matplotlib, the Python counterpart of sportyR.',
  url: 'https://sportypy.sportsdataverse.org',
  baseUrl: '/',
  // Fails the build on a broken link: fix a generated page in its generator
  onBrokenLinks: 'throw',
  favicon: 'img/favicon.png',
  organizationName: 'sportsdataverse',
  projectName: 'sportypy',
  i18n: {defaultLocale: 'en', locales: ['en']},
  // .md pages (the generated reference) are CommonMark, so braces and angle
  // brackets in docstrings and signatures need no MDX escaping
  markdown: {
    format: 'detect',
    hooks: {onBrokenMarkdownLinks: 'throw'},
  },
  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
          // Generated pages have no edit link: they are fixed in the docstrings
          editUrl: ({docPath}) =>
            /^reference\/|^changelog\.md$/.test(docPath)
              ? undefined
              : `https://github.com/sportsdataverse/sportypy/edit/main/website/docs/${docPath}`,
        },
        blog: false,
        theme: {customCss: './src/css/custom.css'},
      } satisfies Preset.Options,
    ],
  ],
  themes: [
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {hashed: true, docsRouteBasePath: '/', indexBlog: false},
    ],
  ],
  themeConfig: {
    // follow the reader's light/dark preference
    colorMode: {respectPrefersColorScheme: true},
    navbar: {
      title: 'sportypy',
      logo: {alt: 'sportypy logo', src: 'img/logo.png'},
      items: [
        {type: 'docSidebar', sidebarId: 'docs', position: 'left', label: 'Docs'},
        {to: '/changelog', label: 'Changelog', position: 'left'},
        {href: 'https://github.com/sportsdataverse/sportyR', label: 'sportyR (R)', position: 'right'},
        {href: 'https://github.com/sportsdataverse/sportypy', label: 'GitHub', position: 'right'},
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'SportsDataverse',
          items: [
            {label: 'sportsdataverse.org', href: 'https://sportsdataverse.org'},
            {label: 'sportyR', href: 'https://github.com/sportsdataverse/sportyR'},
            {label: 'sdvplot', href: 'https://sdvplot.sportsdataverse.org'},
          ],
        },
        {
          title: 'sportypy',
          items: [
            {label: 'PyPI', href: 'https://pypi.org/project/sportypy/'},
            {label: 'Issues', href: 'https://github.com/sportsdataverse/sportypy/issues'},
          ],
        },
      ],
      copyright: `sportypy is released under the GPL-3.0 license.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
