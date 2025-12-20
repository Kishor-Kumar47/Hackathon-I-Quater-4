import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';



const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Your guide to the future of intelligent robotics',
  favicon: 'img/favicon.ico',
 


  future: {
    v4: true,
  },

  // ✅ UPDATED: Your GitHub Pages URL
  url: "https://hackathon-i-quater-4.vercel.app",
  baseUrl: "/",

  // ✅ UPDATED: Your GitHub info
  // organizationName: 'Kishor-Kumar47',
  // projectName: 'Hackathon-I-Quater-4',
  // deploymentBranch: 'gh-pages',
  trailingSlash: false,

  // onBrokenLinks: 'throw',
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/Kishor-Kumar47/Hackathon-I-Quater-4/tree/main/my-website/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          editUrl:
            'https://github.com/Kishor-Kumar47/Hackathon-I-Quater-4/tree/main/my-website/',
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Book',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {to: '/chat', label: 'Chatbot', position: 'left'},
        {to: '/signin', label: 'Sign In', position: 'right'},
        {
          href: 'https://github.com/Kishor-Kumar47/Hackathon-I-Quater-4',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Book',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'LinkedIn',
              href: 'https://www.linkedin.com/in/kishor-kumar-358246271/',
            },
            {
              label: 'My Portfolio',
              href: 'https://kishor-portfolio-lake.vercel.app/',
            },
            {
              label: 'X',
              href: 'https://x.com/KishorK5363784',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/Kishor-Kumar47/Hackathon-I-Quater-4',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI Book by Kishor Kumar - Panaversity Hackathon`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;