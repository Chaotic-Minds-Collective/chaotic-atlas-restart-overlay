fetch('restart-time.json')
  .then(/** Decode the status JSON, rejecting unsuccessful HTTP responses. */ (response) => {
    if (!response.ok) {
      throw new Error(`Failed to load restart status (${response.status})`);
    }
    return response.json();
  })
  .then(/** Render status as text, using unknown for unavailable numeric values. */ (data) => {
    const overlay = document.getElementById('overlay');
    if (!overlay) {
      throw new Error('Restart overlay element was not found');
    }

    const heading = document.createElement('h1');
    const secondsLeft = data.seconds_left === null ? NaN : Number(data.seconds_left);
    heading.textContent = `Server Restarting In: ${Number.isFinite(secondsLeft) ? secondsLeft : 'unknown'}s`;

    const playerCount = document.createElement('p');
    const players = data.player_count === null ? NaN : Number(data.player_count);
    playerCount.textContent = `👥 ${Number.isFinite(players) ? players : 'unknown'} players online`;

    const adminMessage = document.createElement('p');
    adminMessage.textContent = typeof data.admin_message === 'string' ? data.admin_message : '';

    overlay.replaceChildren(heading, playerCount, adminMessage);
  })
  .catch(/** Report fetch, decoding, or rendering failures. */ (error) => {
    console.error('Unable to render restart status:', error);
  });
