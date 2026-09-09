/**
 * DineFlow Enterprise Luxury UI Interactivity & POS Script
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Live Digital Clock (IST / Asia/Kolkata)
    const clockEl = document.getElementById('live-digital-clock');
    if (clockEl) {
        const updateClock = () => {
            const now = new Date();
            const options = {
                timeZone: 'Asia/Kolkata',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: true
            };
            clockEl.textContent = `${now.toLocaleTimeString('en-US', options)} IST`;
        };
        updateClock();
        setInterval(updateClock, 1000);
    }

    // 2. Audio Chime simulation for Kitchen tickets
    window.playKitchenBell = () => {
        try {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(880, ctx.currentTime); // A5 note
            gain.gain.setValueAtTime(0.15, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.6);
            osc.connect(gain);
            gain.connect(ctx.destination);
            osc.start();
            osc.stop(ctx.currentTime + 0.6);
        } catch (e) {
            console.log('AudioContext not permitted yet.');
        }
    };

    // 3. Auto dismiss alerts after 5 seconds
    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.4s ease';
            setTimeout(() => alert.remove(), 400);
        }, 5000);
    });
});
