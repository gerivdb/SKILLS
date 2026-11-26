// Content script universel — Comet phagocytose
// Injecté sur <all_urls> en world ISOLATED, document_start
// Exclusion : *.perplexity.ai/sidecar/*, localhost:*/sidecar*

(function() {
  'use strict';

  const CONFIG = {
    excludePatterns: [
      /\.perplexity\.ai\/sidecar\//,
      /localhost:\*\/\/sidecar\*/,
    ],
    assistantRoleClasses: [/f9bf7997/, /f9bf/],
    userRoleClasses: [/fa81/, /fa81/],
    ackPattern: /^\[ENV6\]\s+ACK\s+([A-Za-z0-9._:-]{4,128})\b/,
    negationPatterns: [
      /Je ne réponds pas/,
      /Je ne suis pas ENV6/,
      /pas \[ENV6\]/,
      /refus/,
    ],
  };

  function isExcluded(url) {
    return CONFIG.excludePatterns.some((re) => re.test(url));
  }

  function getRoleClasses(element) {
    const cls = element.className || '';
    return CONFIG.assistantRoleClasses.some((re) => re.test(cls))
      ? 'assistant'
      : CONFIG.userRoleClasses.some((re) => re.test(cls))
        ? 'user'
        : 'unknown';
  }

  function extractACK(text) {
    const match = text.match(CONFIG.ackPattern);
    if (!match) return null;
    // Test de négation explicite
    if (CONFIG.negationPatterns.some((re) => re.test(text))) {
      return { token: match[1], valid: false, reason: 'negation_phrase_detected' };
    }
    return { token: match[1], valid: true, reason: null };
  }

  function observeDOM() {
    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        for (const node of mutation.addedNodes) {
          if (node.nodeType === Node.ELEMENT_NODE) {
            const role = getRoleClasses(node);
            if (role === 'assistant') {
              const text = node.textContent || '';
              const ack = extractACK(text);
              if (ack && ack.valid) {
                console.log('[COMET-ACK]', {
                  token: ack.token,
                  role,
                  timestamp: new Date().toISOString(),
                });
              }
            }
          }
        }
      }
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });
  }

  if (!isExcluded(window.location.href)) {
    observeDOM();
  }
})();
