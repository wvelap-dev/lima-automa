const { appendFileSync, readFileSync, existsSync, mkdirSync, writeFileSync } = require('fs');
const { join } = require('path');

module.exports = (req, res) => {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'POST') {
    const { codigo_rastreo, restaurante, timestamp, user_agent, language, platform, screen, referrer } = req.body;

    const trackingData = {
      codigo_rastreo,
      restaurante,
      timestamp: timestamp || new Date().toISOString(),
      user_agent: user_agent || req.headers['user-agent'],
      language,
      platform,
      screen,
      referrer: referrer || req.headers.referer || 'direct',
      ip: req.headers['x-forwarded-for'] || req.socket.remoteAddress,
    };

    console.log('[Tracking]', JSON.stringify(trackingData));

    // Intentar guardar en archivo (funciona local, no en Vercel)
    try {
      const dataDir = join(process.cwd(), 'data');
      const dataFile = join(dataDir, 'tracking.json');
      
      mkdirSync(dataDir, { recursive: true });
      
      let tracking = [];
      if (existsSync(dataFile)) {
        try {
          tracking = JSON.parse(readFileSync(dataFile, 'utf8'));
        } catch (e) {
          tracking = [];
        }
      }

      tracking.push(trackingData);
      writeFileSync(dataFile, JSON.stringify(tracking, null, 2));
    } catch (e) {
      // Ignorar error en Vercel (no puede escribir archivos)
    }

    res.status(200).json({ success: true, data: trackingData });
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
};
