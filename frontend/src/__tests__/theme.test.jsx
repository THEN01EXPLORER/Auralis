import React from 'react';
import { render, screen, fireEvent, cleanup } from '@testing-library/react';
import { ThemeProvider, useTheme } from '../contexts/ThemeContext';

function TestComponent() {
  const { theme, toggleTheme } = useTheme();
  return (
    <div>
      <span data-testid="theme-value">{theme}</span>
      <button onClick={toggleTheme}>toggle</button>
    </div>
  );
}

const renderWithProvider = () => {
  return render(
    <ThemeProvider>
      <TestComponent />
    </ThemeProvider>
  );
};

describe('ThemeContext persistence and UI', () => {
  beforeEach(() => {
    localStorage.clear();
    cleanup();
  });

  test('applies theme from localStorage on load', () => {
    localStorage.setItem('auralis-theme', 'dark');
    renderWithProvider();
    expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
    expect(screen.getByTestId('theme-value').textContent).toBe('dark');
  });

  test('falls back to system preference when no localStorage', () => {
    const original = window.matchMedia;
    window.matchMedia = jest.fn().mockImplementation((q) => ({
      matches: true, // prefers dark
      media: q,
      onchange: null,
      addListener: jest.fn(),
      removeListener: jest.fn(),
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
      dispatchEvent: jest.fn(),
    }));

    renderWithProvider();
    expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
    expect(screen.getByTestId('theme-value').textContent).toBe('dark');
    window.matchMedia = original;
  });

  test('toggle updates data-theme and persists to localStorage', () => {
    renderWithProvider();
    const before = document.documentElement.getAttribute('data-theme');
    fireEvent.click(screen.getByText('toggle'));
    const after = document.documentElement.getAttribute('data-theme');
    expect(after).not.toBe(before);
    expect(localStorage.getItem('auralis-theme')).toBe(after);
  });
});
