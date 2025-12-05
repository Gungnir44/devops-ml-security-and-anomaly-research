import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('renders dashboard header', () => {
    render(<App />)
    expect(screen.getByText(/DevOps Security Research Dashboard/i)).toBeInTheDocument()
  })

  it('renders navigation links', () => {
    render(<App />)
    expect(screen.getByText(/Dashboard/i)).toBeInTheDocument()
    expect(screen.getByText(/Users API/i)).toBeInTheDocument()
    expect(screen.getByText(/Data Processing/i)).toBeInTheDocument()
    expect(screen.getByText(/Security Metrics/i)).toBeInTheDocument()
  })

  it('renders footer', () => {
    render(<App />)
    expect(screen.getByText(/Master's Thesis/i)).toBeInTheDocument()
  })
})
