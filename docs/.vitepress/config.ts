import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'AIRS MLOps Lab',
  description: 'Secure MLOps Pipeline Workshop with AI Runtime Security',
  base: '/prisma-airs-mlops-lab/',

  themeConfig: {
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Guide', link: '/guide/' },
      { text: 'Modules', link: '/modules/0-setup' },
      { text: 'GitHub', link: 'https://github.com/airs-labs/prisma-airs-mlops-lab' }
    ],

    sidebar: {
      '/modules/': [
        {
          text: 'Act 1: Build It',
          items: [
            { text: 'Module 0: Setup', link: '/modules/0-setup' },
            { text: 'Module 1: ML Fundamentals', link: '/modules/1-ml-fundamentals' },
            { text: 'Module 2: Train Your Model', link: '/modules/2-train-your-model' },
            { text: 'Module 3: Deploy & Serve', link: '/modules/3-deploy-and-serve' },
          ]
        },
        {
          text: 'Act 2: Understand Security',
          items: [
            { text: 'Module 4: AIRS Deep Dive', link: '/modules/4-airs-deep-dive' },
          ]
        },
        {
          text: 'Act 3: Secure It',
          items: [
            { text: 'Module 5: Integrate AIRS', link: '/modules/5-integrate-airs' },
            { text: 'Module 6: The Threat Zoo', link: '/modules/6-threat-zoo' },
            { text: 'Module 7: Gaps & Poisoning', link: '/modules/7-gaps-and-poisoning' },
          ]
        }
      ],
      '/guide/': [
        {
          text: 'Getting Started',
          items: [
            { text: 'Overview', link: '/guide/' },
            { text: 'Student Setup', link: '/guide/student-setup' },
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/airs-labs/prisma-airs-mlops-lab' }
    ],

    search: {
      provider: 'local'
    },

    footer: {
      message: 'Built with Claude Code',
      copyright: 'MIT License | Palo Alto Networks 2026'
    }
  }
})
