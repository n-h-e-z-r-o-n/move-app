import { WebExtensionBlocker } from '@cliqz/adblocker-webextension';

// Function to initialize the blocker
async function initializeBlocker() {
    try {
        // Initialize blocker with ads only
        let blocker = await WebExtensionBlocker.fromPrebuiltAdsOnly();
        console.log('Ads only blocker initialized');

        // Alternatively, initialize blocker with ads and tracking
        blocker = await WebExtensionBlocker.fromPrebuiltAdsAndTracking();
        console.log('Ads and tracking blocker initialized');

        // Enable the blocker
        blocker.enableBlockingInBrowser();
        console.log('Blocking enabled');
    } catch (error) {
        console.error('Failed to initialize the blocker:', error);
    }
}

// Initialize the blocker when the script runs
initializeBlocker();
