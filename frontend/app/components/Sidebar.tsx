'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

interface NavItem {
  name: string
  href: string
  icon: string
}

const navigation: NavItem[] = [
  { name: 'Content Generator', href: '/', icon: '✨' },
  { name: 'Templates', href: '/templates', icon: '📄' },
  { name: 'History', href: '/history', icon: '📚' },
  { name: 'Analytics', href: '/analytics', icon: '📊' },
  { name: 'Settings', href: '/settings', icon: '⚙️' },
]

export default function Sidebar() {
  const pathname = usePathname()

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="logo">
          <div className="logo-icon">AI</div>
          <div className="logo-text">
            <div className="logo-title">ContentAI</div>
            <div className="logo-subtitle">Enterprise Platform</div>
          </div>
        </div>
      </div>
      
      <nav className="sidebar-nav">
        <ul className="nav-list">
          {navigation.map((item) => {
            const isActive = pathname === item.href
            return (
              <li key={item.name}>
                <Link
                  href={item.href}
                  className={`nav-item ${isActive ? 'active' : ''}`}
                >
                  <span className="nav-icon">{item.icon}</span>
                  <span className="nav-text">{item.name}</span>
                </Link>
              </li>
            )
          })}
        </ul>
      </nav>

      <div className="sidebar-footer">
        <div className="footer-info">
          <div className="footer-label">Powered by</div>
          <div className="footer-value">AWS Bedrock</div>
        </div>
        <div className="footer-badge">STANDs Aligned</div>
      </div>
    </div>
  )
}

