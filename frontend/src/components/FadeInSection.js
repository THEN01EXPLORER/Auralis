import React from 'react';
import { motion } from 'framer-motion';

/**
 * FadeInSection - A reusable component that adds scroll-triggered fade-in animations
 * 
 * @param {React.ReactNode} children - The content to animate
 * @param {number} delay - Optional delay before animation starts (default: 0)
 * @param {number} duration - Animation duration in seconds (default: 0.6)
 * 
 * @example
 * <FadeInSection>
 *   <h2>Your Content Here</h2>
 * </FadeInSection>
 */
const FadeInSection = ({ children, delay = 0, duration = 0.6 }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ 
        duration: duration,
        delay: delay,
        ease: "easeOut"
      }}
    >
      {children}
    </motion.div>
  );
};

export default FadeInSection;
