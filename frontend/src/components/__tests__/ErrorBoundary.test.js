import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ErrorBoundary from '../ErrorBoundary';

// Component that throws an error
const ThrowError = () => {
  throw new Error('Test error');
};

// Component that renders normally
const NormalComponent = () => {
  return <div>Normal content</div>;
};

describe('ErrorBoundary', () => {
  // Suppress console.error for these tests
  beforeAll(() => {
    jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterAll(() => {
    console.error.mockRestore();
  });

  test('renders children when there is no error', () => {
    render(
      <ErrorBoundary>
        <NormalComponent />
      </ErrorBoundary>
    );
    expect(screen.getByText('Normal content')).toBeInTheDocument();
  });

  test('renders error UI when child component throws', () => {
    render(
      <ErrorBoundary>
        <ThrowError />
      </ErrorBoundary>
    );
    expect(screen.getByText('Something went wrong')).toBeInTheDocument();
    expect(screen.getByText(/We're sorry, but something unexpected happened/i)).toBeInTheDocument();
  });

  test('displays refresh button', () => {
    render(
      <ErrorBoundary>
        <ThrowError />
      </ErrorBoundary>
    );
    const refreshButton = screen.getByRole('button', { name: /Refresh Page/i });
    expect(refreshButton).toBeInTheDocument();
  });

  test('refresh button calls window.location.reload', async () => {
    const reloadSpy = jest.fn();
    delete window.location;
    window.location = { reload: reloadSpy };

    render(
      <ErrorBoundary>
        <ThrowError />
      </ErrorBoundary>
    );

    const refreshButton = screen.getByRole('button', { name: /Refresh Page/i });
    await userEvent.click(refreshButton);
    expect(reloadSpy).toHaveBeenCalled();
  });

  test('displays error icon', () => {
    render(
      <ErrorBoundary>
        <ThrowError />
      </ErrorBoundary>
    );
    expect(screen.getByText('⚠️')).toBeInTheDocument();
  });
});
