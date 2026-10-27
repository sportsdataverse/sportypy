import React, {type ReactNode} from 'react';
import Link from '@docusaurus/Link';
import {PageMetadata} from '@docusaurus/theme-common';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

// The site's 404 page, as on the other SportsDataverse docs sites (sdvplot's, ejected with
// `docusaurus swizzle @docusaurus/theme-classic NotFound --eject`). The old Sphinx site's URLs
// (/surfaces/hockey/nhl.html and so on) land here.
export default function NotFound(): ReactNode {
  return (
    <>
      <PageMetadata title="Page not found" />
      <Layout>
        <main className="container margin-vert--xl">
          <div className="row">
            <div className="col col--6 col--offset-3">
              <Heading as="h1" className="sdv-404-title">Page not found</Heading>
              <p>
                Nothing lives at this address. The page may have moved when the docs moved from
                Sphinx to this site, or the link may have a typo.
              </p>
              <p>
                Every sport's surfaces and league classes are in the API reference, and the search
                box at the top of the page finds a class or a method.
              </p>
              <Link className="button button--primary" to="/docs/reference/">
                Go to the API reference
              </Link>
            </div>
          </div>
        </main>
      </Layout>
    </>
  );
}
