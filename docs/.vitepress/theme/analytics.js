// Anonymous counts only. Never include document paths, image URLs or admin data.
let previousPath = ''
export function trackPageView() {
  if (typeof window === 'undefined' || location.origin !== "https://imgbed.webkubor.online" ||
      navigator.doNotTrack === '1' || location.pathname === previousPath) return
  try {
    if (localStorage.getItem('core-analytics') === 'off') return
    previousPath = location.pathname
    void fetch("https://api.webkubor.online/v1/analytics" + '/events', {
      method: 'POST', credentials: 'omit', keepalive: true,
      signal: AbortSignal.timeout(3000),
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ project: 'free-imgbed', event_id: crypto.randomUUID(),
        event: 'page.view', properties: { surface: 'docs' } }),
    }).catch(() => {})
  } catch { /* Counting must never interrupt browsing. */ }
}
