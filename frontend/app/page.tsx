'use client'

import { useState } from 'react'
import axios from 'axios'

interface ContentRequest {
  title: string
  description: string
  tone: string
  language: string
  content_type: string
}

interface ContentResponse {
  hero_section: string
  features: string[]
  benefits: string[]
  seo_meta: {
    title: string
    description: string
    keywords: string[]
  }
  cta: string
  faqs: Array<{ question: string; answer: string }>
  html_content: string
  markdown_content: string
}

type TabType = 'preview' | 'html' | 'markdown' | 'json'

export default function Home() {
  const [formData, setFormData] = useState<ContentRequest>({
    title: '',
    description: '',
    tone: 'professional',
    language: 'en',
    content_type: 'landing_page',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [content, setContent] = useState<ContentResponse | null>(null)
  const [activeTab, setActiveTab] = useState<TabType>('preview')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await axios.post(`${apiUrl}/api/generate`, formData)
      setContent(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to generate content')
    } finally {
      setLoading(false)
    }
  }

  const handleExport = (format: 'html' | 'markdown' | 'json') => {
    if (!content) return

    let blob: Blob
    let filename: string
    let mimeType: string

    if (format === 'html') {
      blob = new Blob([content.html_content], { type: 'text/html' })
      filename = 'content.html'
      mimeType = 'text/html'
    } else if (format === 'markdown') {
      blob = new Blob([content.markdown_content], { type: 'text/markdown' })
      filename = 'content.md'
      mimeType = 'text/markdown'
    } else {
      blob = new Blob([JSON.stringify(content, null, 2)], { type: 'application/json' })
      filename = 'content.json'
      mimeType = 'application/json'
    }

    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="container">
      <div className="header">
        <h1>🚀 Intelligent Content Creator</h1>
        <p>AWS Bedrock-powered content generation platform</p>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-section">
          <div className="form-group">
            <label htmlFor="title">Title *</label>
            <input
              type="text"
              id="title"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              required
              placeholder="Enter page title"
            />
          </div>

          <div className="form-group">
            <label htmlFor="description">Product/Service Description *</label>
            <textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              required
              placeholder="Describe your product or service..."
            />
          </div>

          <div className="form-group">
            <label htmlFor="tone">Tone</label>
            <select
              id="tone"
              value={formData.tone}
              onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
            >
              <option value="professional">Professional</option>
              <option value="casual">Casual</option>
              <option value="friendly">Friendly</option>
              <option value="formal">Formal</option>
              <option value="conversational">Conversational</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="language">Language</label>
            <select
              id="language"
              value={formData.language}
              onChange={(e) => setFormData({ ...formData, language: e.target.value })}
            >
              <option value="en">English</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
              <option value="it">Italian</option>
              <option value="pt">Portuguese</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="content_type">Content Type</label>
            <select
              id="content_type"
              value={formData.content_type}
              onChange={(e) => setFormData({ ...formData, content_type: e.target.value })}
            >
              <option value="landing_page">Landing Page</option>
              <option value="product_page">Product Page</option>
              <option value="blog_post">Blog Post</option>
              <option value="about_page">About Page</option>
            </select>
          </div>
        </div>

        {error && <div className="error">{error}</div>}

        <button type="submit" className="button" disabled={loading}>
          {loading ? 'Generating Content...' : 'Generate Content'}
        </button>
      </form>

      {content && (
        <div className="results-section">
          <h2>Generated Content</h2>
          
          <div className="result-tabs">
            <button
              className={`tab-button ${activeTab === 'preview' ? 'active' : ''}`}
              onClick={() => setActiveTab('preview')}
            >
              Preview
            </button>
            <button
              className={`tab-button ${activeTab === 'html' ? 'active' : ''}`}
              onClick={() => setActiveTab('html')}
            >
              HTML
            </button>
            <button
              className={`tab-button ${activeTab === 'markdown' ? 'active' : ''}`}
              onClick={() => setActiveTab('markdown')}
            >
              Markdown
            </button>
            <button
              className={`tab-button ${activeTab === 'json' ? 'active' : ''}`}
              onClick={() => setActiveTab('json')}
            >
              JSON
            </button>
          </div>

          <div className="result-content">
            {activeTab === 'preview' && (
              <div>
                <h3>Hero Section</h3>
                <p>{content.hero_section}</p>
                
                <h3>Features</h3>
                <ul>
                  {content.features.map((feature, idx) => (
                    <li key={idx}>{feature}</li>
                  ))}
                </ul>
                
                <h3>Benefits</h3>
                <ul>
                  {content.benefits.map((benefit, idx) => (
                    <li key={idx}>{benefit}</li>
                  ))}
                </ul>
                
                <h3>Call to Action</h3>
                <p>{content.cta}</p>
                
                <h3>SEO Meta</h3>
                <p><strong>Title:</strong> {content.seo_meta.title}</p>
                <p><strong>Description:</strong> {content.seo_meta.description}</p>
                <p><strong>Keywords:</strong> {content.seo_meta.keywords.join(', ')}</p>
                
                <h3>FAQs</h3>
                {content.faqs.map((faq, idx) => (
                  <div key={idx}>
                    <p><strong>Q: {faq.question}</strong></p>
                    <p>A: {faq.answer}</p>
                  </div>
                ))}
              </div>
            )}
            {activeTab === 'html' && <pre>{content.html_content}</pre>}
            {activeTab === 'markdown' && <pre>{content.markdown_content}</pre>}
            {activeTab === 'json' && <pre>{JSON.stringify(content, null, 2)}</pre>}
          </div>

          <div className="export-buttons">
            <button className="export-button" onClick={() => handleExport('html')}>
              Export HTML
            </button>
            <button className="export-button" onClick={() => handleExport('markdown')}>
              Export Markdown
            </button>
            <button className="export-button" onClick={() => handleExport('json')}>
              Export JSON
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

