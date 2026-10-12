import { StrictMode, useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';

function App() {
  const [status, setStatus] = useState('Vérification de la connexion…');
  useEffect(() => {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 5000);
    async function checkHealth() {
      try {
        const response = await fetch('/api/health', {
          signal: controller.signal,
        });
        if (!response.ok) throw new Error('Réponse HTTP incorrecte');
        const body: unknown = await response.json();
        if (
          typeof body !== 'object' ||
          body === null ||
          !('status' in body) ||
          body.status !== 'ok'
        ) {
          throw new Error('Réponse API inattendue');
        }
        setStatus('API connectée');
      } catch {
        if (!cancelled)
          setStatus(
            'API indisponible. Vérifie que le backend est lancé, puis recharge la page.',
          );
      } finally {
        clearTimeout(timer);
      }
    }
    let cancelled = false;
    void checkHealth();
    return () => {
      cancelled = true;
      controller.abort();
      clearTimeout(timer);
    };
  }, []);
  return (
    <main>
      <p>Projet personnel — en cours</p>
      <h1>PretApp</h1>
      <p>Gestion de prêts et de réservations de matériel.</p>
      <p role="status" aria-live="polite">
        {status}
      </p>
      <p>Première étape : relier une interface React à une API FastAPI.</p>
    </main>
  );
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
