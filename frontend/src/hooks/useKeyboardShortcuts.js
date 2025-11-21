import { useEffect } from 'react';

export const useKeyboardShortcuts = (shortcuts) => {
  useEffect(() => {
    const handleKeyDown = (event) => {
      // Check if user is typing in an input/textarea
      if (
        event.target.tagName === 'INPUT' ||
        event.target.tagName === 'TEXTAREA' ||
        event.target.isContentEditable
      ) {
        // Allow shortcuts with Ctrl/Cmd
        if (!event.ctrlKey && !event.metaKey) {
          return;
        }
      }

      const key = event.key.toLowerCase();
      const ctrl = event.ctrlKey || event.metaKey;
      const shift = event.shiftKey;
      const alt = event.altKey;

      // Find matching shortcut
      const shortcut = shortcuts.find((s) => {
        const keyMatch = s.key.toLowerCase() === key;
        const ctrlMatch = s.ctrl === undefined ? false : s.ctrl === ctrl;
        const shiftMatch = s.shift === undefined ? false : s.shift === shift;
        const altMatch = s.alt === undefined ? false : s.alt === alt;

        return keyMatch && (s.ctrl === undefined || ctrlMatch) && 
               (s.shift === undefined || shiftMatch) && 
               (s.alt === undefined || altMatch);
      });

      if (shortcut) {
        event.preventDefault();
        shortcut.action();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [shortcuts]);
};


