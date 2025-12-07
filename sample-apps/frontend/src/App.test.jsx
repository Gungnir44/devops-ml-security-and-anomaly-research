import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('renders dashboard header', () => {
    render(<App />)
    expect(
      screen.getByText(/DevOps Security Research Dashboard/i)
    ).toBeInTheDocument()
  })

  it('renders navigation links', () => {
    render(<App />)
    // Use getByRole to specifically target navigation links (not header text containing "Dashboard")
    expect(
      screen.getByRole('link', { name: /^Dashboard$/i })
    ).toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Users API/i })).toBeInTheDocument()
    expect(
      screen.getByRole('link', { name: /Data Processing/i })
    ).toBeInTheDocument()
    expect(
      screen.getByRole('link', { name: /Security Metrics/i })
    ).toBeInTheDocument()
  })

  it('renders footer', () => {
    render(<App />)
    expect(screen.getByText(/Master's Thesis/i)).toBeInTheDocument()
  })
})
