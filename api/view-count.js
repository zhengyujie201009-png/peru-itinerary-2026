const COUNTER_URL = 'https://api.counterapi.dev/v1/peru-itinerary-2026-yujie/page-views';

module.exports = async function handler(request, response) {
  response.setHeader('Cache-Control', 'no-store');

  try {
    const increment = request.query.increment === '1';
    const counterResponse = await fetch(`${COUNTER_URL}${increment ? '/up' : ''}`);
    if (!counterResponse.ok) throw new Error(`Counter returned ${counterResponse.status}`);

    const result = await counterResponse.json();
    response.status(200).json({ count: Number(result.count || 0) });
  } catch (error) {
    response.status(502).json({ error: 'counter_unavailable' });
  }
};
