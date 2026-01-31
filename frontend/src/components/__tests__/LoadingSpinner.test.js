import React from 'react';
import { render, screen } from '@testing-library/react';
import LoadingSpinner from '../LoadingSpinner';

describe('LoadingSpinner', () => {
  test('renders with default message', () => {
    render(<LoadingSpinner />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  test('renders with custom message', () => {
    render(<LoadingSpinner message="Analyzing contract..." />);
    expect(screen.getByText('Analyzing contract...')).toBeInTheDocument();
  });

  test('renders spinner element', () => {
    const { container } = render(<LoadingSpinner />);
    const spinner = container.querySelector('.spinner');
    expect(spinner).toBeInTheDocument();
  });

  test('renders progress bar when progress prop is provided', () => {
    const { container } = render(<LoadingSpinner progress={50} />);
    const progressBar = container.querySelector('.progress-bar');
    expect(progressBar).toBeInTheDocument();
    expect(progressBar).toHaveStyle({ width: '50%' });
  });

  test('does not render progress bar when progress is null', () => {
    const { container } = render(<LoadingSpinner progress={null} />);
    const progressBar = container.querySelector('.progress-bar');
    expect(progressBar).not.toBeInTheDocument();
  });

  test('updates progress bar width based on progress prop', () => {
    const { container, rerender } = render(<LoadingSpinner progress={25} />);
    let progressBar = container.querySelector('.progress-bar');
    expect(progressBar).toHaveStyle({ width: '25%' });

    rerender(<LoadingSpinner progress={75} />);
    progressBar = container.querySelector('.progress-bar');
    expect(progressBar).toHaveStyle({ width: '75%' });
  });

  test('renders loading container', () => {
    const { container } = render(<LoadingSpinner />);
    const loadingContainer = container.querySelector('.loading-spinner-container');
    expect(loadingContainer).toBeInTheDocument();
  });
});
