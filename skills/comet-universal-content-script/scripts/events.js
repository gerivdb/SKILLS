// Events.js — Capture d'événements DOM universels
// Injecté sur <all_urls> en world ISOLATED, document_start, all_frames
// Exclusion : *.perplexity.ai/sidecar/*, localhost:*/sidecar/*

(function() {
  'use strict';

  const EVENT_TYPES = ['click', 'submit', 'keydown', 'popstate', 'hashchange'];

  function isExcluded(url) {
    return [
      /\.perplexity\.ai\/sidecar\//,
      /localhost:\*\/\/sidecar\*/,
    ].some((re) => re.test(url));
  }

  function captureEvent(event) {
    const target = event.target;
    if (!target) return;

    const eventData = {
      type: event.type,
      timestamp: new Date().toISOString(),
      url: window.location.href,
      target: {
        tagName: target.tagName,
        className: target.className || '',
        id: target.id || '',
        textContent: (target.textContent || '').substring(0, 200),
      },
    };

    // Envoi vers le background script via runtime.sendMessage
    if (typeof chrome !== 'undefined' && chrome.runtime) {
      chrome.runtime.sendMessage({
        type: 'DOM_EVENT',
        data: eventData,
      }).catch(() => {
        // Ignorer les erreurs d'envoi (background peut ne pas être prêt)
      });
    }
  }

  if (!isExcluded(window.location.href)) {
    EVENT_TYPES.forEach((evt) => {
      document.addEventListener(evt, captureEvent, true);
    });

    // Surveillance des changements d'URL (SPA)
    let lastUrl = window.location.href;
    const urlObserver = new MutationObserver(() => {
      if (window.location.href !== lastUrl) {
        lastUrl = window.location.href;
        captureEvent({ type: 'urlchange', target: window.location });
      }
    });
    urlObserver.observe(document, { subtree: true, childList: true });
  }
})();
