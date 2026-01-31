/**
 * FadeInSection Component Usage Examples
 * 
 * This file demonstrates various ways to use the FadeInSection component
 * for scroll-triggered animations in your React application.
 */

import React from 'react';
import FadeInSection from './components/FadeInSection';

// ============================================================
// EXAMPLE 1: Basic Usage - Wrap any content
// ============================================================
function BasicExample() {
  return (
    <FadeInSection>
      <h2>This heading will fade in when scrolled into view</h2>
      <p>All content inside FadeInSection animates together.</p>
    </FadeInSection>
  );
}

// ============================================================
// EXAMPLE 2: Multiple Sections with Staggered Delays
// ============================================================
function StaggeredExample() {
  return (
    <div>
      <FadeInSection delay={0}>
        <div className="card">Card 1 - appears first</div>
      </FadeInSection>
      
      <FadeInSection delay={0.2}>
        <div className="card">Card 2 - appears 0.2s later</div>
      </FadeInSection>
      
      <FadeInSection delay={0.4}>
        <div className="card">Card 3 - appears 0.4s later</div>
      </FadeInSection>
    </div>
  );
}

// ============================================================
// EXAMPLE 3: Features Grid (Like FeatureShowcase.js)
// ============================================================
function FeaturesGridExample() {
  const features = [
    { title: 'Feature 1', description: 'Description 1' },
    { title: 'Feature 2', description: 'Description 2' },
    { title: 'Feature 3', description: 'Description 3' },
  ];

  return (
    <div className="features-section">
      {/* Animate the header */}
      <FadeInSection>
        <div className="section-header">
          <h2>Amazing Features</h2>
          <p>Check out what we offer</p>
        </div>
      </FadeInSection>

      {/* Animate each feature card with staggered timing */}
      <div className="features-grid">
        {features.map((feature, index) => (
          <FadeInSection key={index} delay={index * 0.1}>
            <div className="feature-card">
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </div>
          </FadeInSection>
        ))}
      </div>
    </div>
  );
}

// ============================================================
// EXAMPLE 4: Hero Section with Custom Duration
// ============================================================
function HeroExample() {
  return (
    <section className="hero">
      <FadeInSection duration={0.8}>
        <h1>Welcome to Our Platform</h1>
      </FadeInSection>
      
      <FadeInSection delay={0.3} duration={0.8}>
        <p className="subtitle">Building the future, one line at a time</p>
      </FadeInSection>
      
      <FadeInSection delay={0.6} duration={0.6}>
        <button className="cta-button">Get Started</button>
      </FadeInSection>
    </section>
  );
}

// ============================================================
// EXAMPLE 5: Nested Content
// ============================================================
function NestedExample() {
  return (
    <FadeInSection>
      <div className="content-section">
        <h2>Section Title</h2>
        <div className="inner-content">
          <p>All of this content animates as one unit.</p>
          <ul>
            <li>Item 1</li>
            <li>Item 2</li>
            <li>Item 3</li>
          </ul>
        </div>
      </div>
    </FadeInSection>
  );
}

// ============================================================
// EXAMPLE 6: Image Gallery
// ============================================================
function GalleryExample() {
  const images = [
    '/img1.jpg',
    '/img2.jpg',
    '/img3.jpg',
    '/img4.jpg',
  ];

  return (
    <div className="gallery">
      {images.map((img, index) => (
        <FadeInSection key={index} delay={index * 0.15}>
          <img src={img} alt={`Gallery item ${index + 1}`} />
        </FadeInSection>
      ))}
    </div>
  );
}

// ============================================================
// EXAMPLE 7: Stats Counter Section
// ============================================================
function StatsExample() {
  const stats = [
    { value: '1000+', label: 'Users' },
    { value: '50+', label: 'Countries' },
    { value: '99.9%', label: 'Uptime' },
    { value: '24/7', label: 'Support' },
  ];

  return (
    <div className="stats-section">
      <FadeInSection>
        <h2>Our Impact</h2>
      </FadeInSection>
      
      <div className="stats-grid">
        {stats.map((stat, index) => (
          <FadeInSection key={index} delay={index * 0.1}>
            <div className="stat-card">
              <div className="stat-value">{stat.value}</div>
              <div className="stat-label">{stat.label}</div>
            </div>
          </FadeInSection>
        ))}
      </div>
    </div>
  );
}

// ============================================================
// EXAMPLE 8: Testimonials
// ============================================================
function TestimonialsExample() {
  const testimonials = [
    { text: 'Great product!', author: 'John Doe' },
    { text: 'Amazing service!', author: 'Jane Smith' },
    { text: 'Highly recommend!', author: 'Bob Johnson' },
  ];

  return (
    <div className="testimonials">
      <FadeInSection>
        <h2>What Our Customers Say</h2>
      </FadeInSection>
      
      {testimonials.map((testimonial, index) => (
        <FadeInSection key={index} delay={index * 0.2}>
          <blockquote className="testimonial-card">
            <p>"{testimonial.text}"</p>
            <cite>— {testimonial.author}</cite>
          </blockquote>
        </FadeInSection>
      ))}
    </div>
  );
}

// ============================================================
// HOW TO USE IN YOUR HOME.JS / LANDING PAGE:
// ============================================================
/*

import FadeInSection from '../components/FadeInSection';

function Home() {
  return (
    <div className="home">
      
      // Wrap your FeatureShowcase or any section:
      <FadeInSection>
        <FeatureShowcase />
      </FadeInSection>
      
      // Or wrap individual elements with staggered delays:
      <div className="features-section">
        <FadeInSection>
          <h2>Features Section</h2>
        </FadeInSection>
        
        <FadeInSection delay={0.2}>
          <StatsDashboard />
        </FadeInSection>
        
        <FadeInSection delay={0.4}>
          <VulnerabilityReport />
        </FadeInSection>
      </div>
    </div>
  );
}

*/

export {
  BasicExample,
  StaggeredExample,
  FeaturesGridExample,
  HeroExample,
  NestedExample,
  GalleryExample,
  StatsExample,
  TestimonialsExample,
};
