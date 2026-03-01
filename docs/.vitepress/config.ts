import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid(
  defineConfig({
    title: 'AIRS MLOps Lab',
    description: 'Secure MLOps Pipeline Workshop with AI Runtime Security',
    base: '/prisma-airs-mlops-lab/',

    themeConfig: {
      nav: [
        { text: 'Home', link: '/' },
        { text: 'Guide', link: '/guide/' },
        { text: 'How It Works', link: '/how-it-works' },
        { text: 'Modules', link: '/modules' },
        { text: 'GitHub', link: 'https://github.com/airs-labs/prisma-airs-mlops-lab' }
      ],

      sidebar: [
        {
          text: 'Guide',
          items: [
            { text: 'What You\'ll Build', link: '/guide/' },
            { text: 'Student Setup', link: '/guide/student-setup' },
          ]
        },
        { text: 'How It Works', link: '/how-it-works' },
        { text: 'Modules', link: '/modules' },
      ],

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
)
