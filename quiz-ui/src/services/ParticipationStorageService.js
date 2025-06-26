export default {
  clear() {
    window.localStorage.clear();
  },
  savePlayerName(playerName) {
    window.localStorage.setItem('playerName', playerName);
  },
  getPlayerName() {
    return window.localStorage.getItem('playerName');
  },
  saveParticipationScore(score) {
    window.localStorage.setItem('participationScore', score);
  },
  getParticipationScore() {
    return parseInt(window.localStorage.getItem('participationScore')) || 0;
  },
};
