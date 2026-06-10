// @ts-check
const { test, expect } = require('@playwright/test');

// All tests run in fresh contexts (no shared localStorage), so each one
// starts on Day 1 of whatever plan it loads.
//
// v0.5 added an onboarding overlay that intercepts first load. Tests that
// don't specifically exercise onboarding pre-stamp the flag so the app
// boots straight into the daily view. The onboarding-specific tests skip
// this beforeEach by living in their own describe block.
test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem('ow_onboarded_v05', '1');
  });
});

test.describe('Operation Watchman — smoke', () => {
  test('loads the watchman-90 plan and renders Day 1', async ({ page }) => {
    await page.goto('/index.html');

    // Header reflects the loaded plan, not the hardcoded fallback alone.
    await expect(page.locator('header h1')).toHaveText('Operation Watchman');
    await expect(page.locator('#dayBanner')).toContainText('Day 1 of 90');
    await expect(page.locator('#progressPct')).toContainText('Day 1 of 90');

    // Five readings, six disciplines from the plan.
    await expect(page.locator('#readingsList .check-item')).toHaveCount(5);
    await expect(page.locator('#discList .check-item')).toHaveCount(6);

    // Day 1 specifically has refs for every reading.
    const morning = page.locator('.check-item[data-key="morning_wisdom"] .check-sub');
    await expect(morning).toContainText('Proverbs 1');
  });

  test('checking an item persists across reload', async ({ page }) => {
    await page.goto('/index.html');
    const item = page.locator('.check-item[data-key="morning_wisdom"]');
    await item.click();
    await expect(item).toHaveClass(/checked/);
    await expect(page.locator('#readingsBadge')).toHaveText('1 / 5');

    await page.reload();
    await expect(page.locator('.check-item[data-key="morning_wisdom"]'))
      .toHaveClass(/checked/);
    await expect(page.locator('#readingsBadge')).toHaveText('1 / 5');
  });

  test('check items are keyboard-accessible checkboxes', async ({ page }) => {
    await page.goto('/index.html');
    const item = page.locator('.check-item[data-key="morning_wisdom"]');
    await expect(item).toHaveAttribute('role', 'checkbox');
    await expect(item).toHaveAttribute('aria-checked', 'false');

    await item.focus();
    await page.keyboard.press(' ');
    await expect(item).toHaveClass(/checked/);
    await expect(item).toHaveAttribute('aria-checked', 'true');

    await page.keyboard.press('Enter');
    await expect(item).not.toHaveClass(/checked/);
    await expect(item).toHaveAttribute('aria-checked', 'false');
  });

  test('streak increments after a fully complete day', async ({ page }) => {
    await page.goto('/index.html');
    // Tick every reading + discipline for today.
    const items = page.locator('.check-item');
    const n = await items.count();
    for (let i = 0; i < n; i++) await items.nth(i).click();
    await expect(page.locator('#streakNum')).toHaveText('1');
  });
});

test.describe('Operation Watchman — journal', () => {
  test('opens, autosaves, persists across reload, exports', async ({ page }) => {
    await page.goto('/index.html');

    await page.locator('#journalBtn').click();
    const modal = page.locator('#journalModal');
    await expect(modal).toHaveClass(/visible/);

    // Day 1 has a reflection prompt.
    await expect(page.locator('#modalPromptText')).not.toHaveText('');

    const text = 'Stood the post today. Held the line.';
    await page.locator('#modalText').fill(text);
    // Skip the transient "Saving..." state — race-prone; just wait for the
    // eventual "Saved" state after the 600ms debounce.
    await expect(page.locator('#modalSaved')).toHaveText('Saved');

    // Close, reload, reopen — text persists.
    await page.locator('#modalClose').click();
    await expect(modal).not.toHaveClass(/visible/);
    await page.reload();
    await page.locator('#journalBtn').click();
    await expect(page.locator('#modalText')).toHaveValue(text);

    // Export triggers a markdown download.
    const downloadPromise = page.waitForEvent('download');
    await page.locator('#btnExport').click();
    const download = await downloadPromise;
    expect(download.suggestedFilename()).toMatch(/^watchman-90-journal-\d{4}-\d{2}-\d{2}\.md$/);
  });

  test('Escape closes the modal', async ({ page }) => {
    await page.goto('/index.html');
    await page.locator('#journalBtn').click();
    await expect(page.locator('#journalModal')).toHaveClass(/visible/);
    await page.keyboard.press('Escape');
    await expect(page.locator('#journalModal')).not.toHaveClass(/visible/);
  });
});

test.describe('Operation Watchman — plan switcher', () => {
  test('switches to proverbs-31 and keeps data isolated', async ({ page }) => {
    await page.goto('/index.html');

    // Seed some state in the watchman plan so we can prove it survives.
    await page.locator('.check-item[data-key="morning_wisdom"]').click();
    await page.locator('#journalBtn').click();
    await page.locator('#modalText').fill('Watchman day one entry.');
    await page.waitForTimeout(800); // autosave debounce
    await page.locator('#modalClose').click();

    // Open the plans modal and confirm both plans are listed.
    await page.locator('#plansBtn').click();
    await expect(page.locator('#plansModal')).toHaveClass(/visible/);
    await expect(page.locator('#plansBody .plan-card')).toHaveCount(2);

    // Switch to proverbs-31. The confirm() must be accepted before click resolves.
    page.once('dialog', d => d.accept());
    await page.locator('.plan-card .btn-activate').click();
    // toHaveText polls until the reload completes and re-renders the header.
    await expect(page.locator('header h1')).toHaveText('Proverbs in 31');
    await expect(page.locator('#dayBanner')).toContainText('Day 1 of 31');
    await expect(page.locator('#readingsList .check-item')).toHaveCount(1);
    // proverbs-31 has zero disciplines — that card is hidden entirely.
    await expect(page.locator('#discCard')).toBeHidden();

    // The previous plan's check did NOT carry over.
    await expect(page.locator('.check-item[data-key="proverb_of_day"]'))
      .not.toHaveClass(/checked/);

    // The previous plan's journal entry did NOT carry over.
    await page.locator('#journalBtn').click();
    await expect(page.locator('#modalText')).toHaveValue('');
    await page.locator('#modalClose').click();

    // Switch back and verify the watchman data survived.
    await page.locator('#plansBtn').click();
    page.once('dialog', d => d.accept());
    await page.locator('.plan-card .btn-activate').click();
    await expect(page.locator('header h1')).toHaveText('Operation Watchman');
    await expect(page.locator('.check-item[data-key="morning_wisdom"]'))
      .toHaveClass(/checked/);
    await page.locator('#journalBtn').click();
    await expect(page.locator('#modalText')).toHaveValue('Watchman day one entry.');
  });
});

test.describe('Operation Watchman — migration', () => {
  test('legacy v0.3 keys are copied into the watchman-90 namespace', async ({ page }) => {
    // Seed unprefixed keys BEFORE the app boots.
    await page.addInitScript(() => {
      // Local date, matching the app's toLocalISO (not UTC toISOString).
      const d = new Date();
      const today = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
      localStorage.setItem('ow_start_date', today);
      localStorage.setItem('ow_daily_' + today, JSON.stringify({ morning_wisdom: true }));
      localStorage.setItem('ow_journal_' + today, 'Legacy reflection text.');
      localStorage.setItem('ow_last_checked', today);
    });

    await page.goto('/index.html');

    // The check from the legacy daily key should be honored.
    await expect(page.locator('.check-item[data-key="morning_wisdom"]'))
      .toHaveClass(/checked/);

    // Journal should show the migrated text.
    await page.locator('#journalBtn').click();
    await expect(page.locator('#modalText')).toHaveValue('Legacy reflection text.');

    // New namespaced keys exist, the flag is set, and originals remain.
    const ls = await page.evaluate(() => {
      const out = {};
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i);
        out[k] = localStorage.getItem(k);
      }
      return out;
    });
    expect(ls).toHaveProperty('ow_migrated_v04', '1');
    expect(ls).toHaveProperty('ow_active_plan', 'watchman-90');
    expect(Object.keys(ls).some(k => k.startsWith('ow_plan_watchman-90_journal_'))).toBe(true);
    expect(Object.keys(ls).some(k => k.startsWith('ow_plan_watchman-90_daily_'))).toBe(true);
    expect(ls).toHaveProperty('ow_start_date'); // original preserved
  });
});

test.describe('Operation Watchman — v0.5 features', () => {
  test('weekly confession anchor is visible on Day 1', async ({ page }) => {
    await page.goto('/index.html');
    const card = page.locator('#confessionCard');
    await expect(card).toBeVisible();
    await expect(page.locator('#confTitle')).toHaveText('Of the Holy Scriptures');
    await expect(page.locator('#confChapter')).toContainText('Chapter 1');
    await expect(page.locator('#confChapter')).toContainText('Week 1');
  });

  test('USMC Ministries footer link is present', async ({ page }) => {
    await page.goto('/index.html');
    const link = page.locator('.app-footer a').first();
    await expect(link).toHaveText('USMC Ministries');
    await expect(link).toHaveAttribute('href', 'https://usmcmin.org');
  });

  test('Lord\'s Day banner toggles by weekday', async ({ page }) => {
    await page.goto('/index.html');
    const isSunday = await page.evaluate(() => new Date().getDay() === 0);
    const banner = page.locator('#lordsDay');
    if (isSunday) {
      await expect(banner).toBeVisible();
    } else {
      await expect(banner).toBeHidden();
    }
  });

  test('anchor prayer persists and shows in journal', async ({ page }) => {
    // Pre-seed the anchor so we don't have to drive the prompt() dialog.
    await page.addInitScript(() => {
      localStorage.setItem('ow_plan_watchman-90_anchor', 'For my marriage and my sons.');
    });
    await page.goto('/index.html');
    await page.locator('#journalBtn').click();
    const anchorBox = page.locator('#anchorDisplay');
    await expect(anchorBox).toBeVisible();
    await expect(anchorBox).not.toHaveClass(/empty/);
    await expect(page.locator('#anchorText')).toHaveText('For my marriage and my sons.');
  });

  test('graduation screen renders past Day 90', async ({ page }) => {
    // Backdate start so today is Day 95.
    await page.addInitScript(() => {
      const d = new Date();
      d.setDate(d.getDate() - 94);
      const y = d.getFullYear();
      const m = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      localStorage.setItem('ow_plan_watchman-90_start_date', `${y}-${m}-${day}`);
    });
    await page.goto('/index.html');
    await expect(page.locator('#graduation')).toBeVisible();
    await expect(page.locator('#gradTitle')).toContainText('stood your post');
    // Daily cards step aside for the debrief.
    await expect(page.locator('#readingsCard')).toBeHidden();
    await expect(page.locator('#discCard')).toBeHidden();
  });
});

test.describe('Operation Watchman — onboarding', () => {
  // These tests need a virgin localStorage; override the global beforeEach
  // by clearing the flag it set. addInitScript runs on EVERY navigation
  // (including page.reload()), so use a one-shot sentinel — otherwise the
  // reload step would wipe a flag the test just verified was set.
  test.beforeEach(async ({ page }) => {
    await page.addInitScript(() => {
      if (localStorage.getItem('__test_cleared_onboard') !== '1') {
        localStorage.removeItem('ow_onboarded_v05');
        localStorage.setItem('__test_cleared_onboard', '1');
      }
    });
  });

  test('onboarding overlay shows on first load', async ({ page }) => {
    await page.goto('/index.html');
    await expect(page.locator('#onboardOverlay')).toBeVisible();
    await expect(page.locator('#onboardHeading')).toContainText('Operation Watchman');
  });

  test('begin button saves anchor, stamps start date, and dismisses', async ({ page }) => {
    await page.goto('/index.html');
    await page.locator('#onboardAnchor').fill('For my son to know the Lord.');
    await page.locator('#onboardBegin').click();
    await expect(page.locator('#onboardOverlay')).toBeHidden();

    // Anchor persisted under the active plan
    const anchor = await page.evaluate(() =>
      localStorage.getItem('ow_plan_watchman-90_anchor')
    );
    expect(anchor).toBe('For my son to know the Lord.');

    // Flag set; next reload skips onboarding
    const flag = await page.evaluate(() => localStorage.getItem('ow_onboarded_v05'));
    expect(flag).toBe('1');

    await page.reload();
    await expect(page.locator('#onboardOverlay')).toBeHidden();
    await expect(page.locator('#dayBanner')).toContainText('Day 1 of 90');
  });
});
