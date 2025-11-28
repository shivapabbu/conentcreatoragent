import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Sidebar from './components/Sidebar'
import Header from './components/Header'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'ContentAI - Enterprise Content Generation Platform',
  description: 'AWS Bedrock-powered intelligent content creation platform with STANDs alignment',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="app-container">
          <Sidebar />
          <div className="main-content">
            <Header />
            <main className="content-area">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  )
}
