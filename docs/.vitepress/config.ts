import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid(
  defineConfig({
    title: 'AIRS MLOps Lab',
    description: 'Secure MLOps Pipeline Workshop with AI Runtime Security',
    base: '/prisma-airs-mlops-lab/',

    locales: {
      root: {
        label: 'English',
        lang: 'en',
      },
      es: {
        label: 'Español',
        lang: 'es-MX',
        link: '/es/',
        title: 'AIRS MLOps Lab',
        description: 'Workshop de Pipeline MLOps Seguro con AI Runtime Security',
        themeConfig: {
          nav: [
            { text: 'Inicio', link: '/es/' },
            { text: 'Guía', link: '/es/guide/' },
            { text: 'Cómo Funciona', link: '/es/how-it-works' },
            { text: 'Módulos', link: '/es/modules' },
            { text: 'GitHub', link: 'https://github.com/airs-labs/prisma-airs-mlops-lab' }
          ],
          sidebar: [
            {
              text: 'Guía',
              items: [
                { text: 'Lo Que Vas a Construir', link: '/es/guide/' },
                { text: 'Configuración del Estudiante', link: '/es/guide/student-setup' },
              ]
            },
            { text: 'Cómo Funciona', link: '/es/how-it-works' },
            { text: 'Módulos', link: '/es/modules' },
          ],
          outline: { label: 'En esta página' },
          docFooter: {
            prev: 'Anterior',
            next: 'Siguiente'
          },
          lastUpdated: { text: 'Última actualización' },
          footer: {
            message: 'Construido con Claude Code',
            copyright: 'Licencia MIT | Palo Alto Networks 2026'
          }
        }
      },
      pt: {
        label: 'Português',
        lang: 'pt-BR',
        link: '/pt/',
        title: 'AIRS MLOps Lab',
        description: 'Workshop de Pipeline MLOps Seguro com AI Runtime Security',
        themeConfig: {
          nav: [
            { text: 'Início', link: '/pt/' },
            { text: 'Guia', link: '/pt/guide/' },
            { text: 'Como Funciona', link: '/pt/how-it-works' },
            { text: 'Módulos', link: '/pt/modules' },
            { text: 'GitHub', link: 'https://github.com/airs-labs/prisma-airs-mlops-lab' }
          ],
          sidebar: [
            {
              text: 'Guia',
              items: [
                { text: 'O Que Você Vai Construir', link: '/pt/guide/' },
                { text: 'Configuração do Estudante', link: '/pt/guide/student-setup' },
              ]
            },
            { text: 'Como Funciona', link: '/pt/how-it-works' },
            { text: 'Módulos', link: '/pt/modules' },
          ],
          outline: { label: 'Nesta página' },
          docFooter: {
            prev: 'Anterior',
            next: 'Próximo'
          },
          lastUpdated: { text: 'Última atualização' },
          footer: {
            message: 'Construído com Claude Code',
            copyright: 'Licença MIT | Palo Alto Networks 2026'
          }
        }
      }
    },

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
        provider: 'local',
        options: {
          locales: {
            es: {
              translations: {
                button: { buttonText: 'Buscar', buttonAriaLabel: 'Buscar' },
                modal: {
                  noResultsText: 'No se encontraron resultados',
                  resetButtonTitle: 'Limpiar búsqueda',
                  footer: { selectText: 'seleccionar', navigateText: 'navegar', closeText: 'cerrar' }
                }
              }
            },
            pt: {
              translations: {
                button: { buttonText: 'Pesquisar', buttonAriaLabel: 'Pesquisar' },
                modal: {
                  noResultsText: 'Nenhum resultado encontrado',
                  resetButtonTitle: 'Limpar pesquisa',
                  footer: { selectText: 'selecionar', navigateText: 'navegar', closeText: 'fechar' }
                }
              }
            }
          }
        }
      },

      footer: {
        message: 'Built with Claude Code',
        copyright: 'MIT License | Palo Alto Networks 2026'
      }
    }
  })
)
