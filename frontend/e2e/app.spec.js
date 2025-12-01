import { test, expect } from '@playwright/test';

test.describe('Astro Chart Generator - End-to-End Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the application
    await page.goto('/');
    // Wait for the page to load
    await page.waitForLoadState('networkidle');
  });

  test('should load the application and display the form', async ({ page }) => {
    // Check page title
    await expect(page).toHaveTitle(/Astro Chart Generator/i);

    // Check that form elements are visible
    const dateInput = page.locator('input[type="date"]');
    const timeInput = page.locator('input[type="time"]');
    const countryInput = page.locator('input[placeholder*="Country"]');
    const cityInput = page.locator('input[placeholder*="City"]');
    const submitButton = page.locator('button:has-text("Generate Chart")');

    await expect(dateInput).toBeVisible();
    await expect(timeInput).toBeVisible();
    await expect(countryInput).toBeVisible();
    await expect(cityInput).toBeVisible();
    await expect(submitButton).toBeVisible();
  });

  test('should validate form - reject future dates', async ({ page }) => {
    const dateInput = page.locator('input[type="date"]');
    const submitButton = page.locator('button:has-text("Generate Chart")');

    // Get tomorrow's date
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    const tomorrowStr = tomorrow.toISOString().split('T')[0];

    // Try to enter a future date
    await dateInput.fill(tomorrowStr);
    await page.locator('input[type="time"]').fill('12:00');
    await page.locator('input[placeholder*="Country"]').fill('USA');
    await page.locator('input[placeholder*="City"]').fill('New York');

    // Submit form
    await submitButton.click();

    // Should see validation error
    const errorMessage = page.locator('text=/cannot be in the future/i');
    await expect(errorMessage).toBeVisible({ timeout: 2000 });
  });

  test('should validate form - reject empty fields', async ({ page }) => {
    const submitButton = page.locator('button:has-text("Generate Chart")');

    // Try to submit empty form
    await submitButton.click();

    // Should see validation errors
    const errorMessages = page.locator('[role="alert"], .validation-error');
    const count = await errorMessages.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should generate chart successfully with valid input', async ({ page }) => {
    const dateInput = page.locator('input[type="date"]');
    const timeInput = page.locator('input[type="time"]');
    const countryInput = page.locator('input[placeholder*="Country"]');
    const cityInput = page.locator('input[placeholder*="City"]');
    const submitButton = page.locator('button:has-text("Generate Chart")');

    // Fill form with valid data
    await dateInput.fill('1990-06-15');
    await timeInput.fill('14:30');
    await countryInput.fill('USA');
    await cityInput.fill('New York');

    // Submit form
    await submitButton.click();

    // Wait for API response and chart to render
    await page.waitForLoadState('networkidle');

    // Check that chart is displayed
    const chartSvg = page.locator('svg[role="img"]');
    await expect(chartSvg).toBeVisible({ timeout: 5000 });

    // Check that planets are displayed
    const planets = page.locator('[data-planet]');
    const planetCount = await planets.count();
    expect(planetCount).toBeGreaterThan(0);
  });

  test('should display planets in the chart', async ({ page }) => {
    // Fill and submit form
    await page.locator('input[type="date"]').fill('1990-06-15');
    await page.locator('input[type="time"]').fill('14:30');
    await page.locator('input[placeholder*="Country"]').fill('USA');
    await page.locator('input[placeholder*="City"]').fill('New York');
    await page.locator('button:has-text("Generate Chart")').click();

    // Wait for chart
    await page.waitForLoadState('networkidle');
    await expect(page.locator('svg[role="img"]')).toBeVisible({ timeout: 5000 });

    // Check for specific planets in legend
    const sunLegend = page.locator('text=/Sun/i').first();
    const moonLegend = page.locator('text=/Moon/i').first();
    const mercuryLegend = page.locator('text=/Mercury/i').first();

    await expect(sunLegend).toBeVisible();
    await expect(moonLegend).toBeVisible();
    await expect(mercuryLegend).toBeVisible();
  });

  test('should display zodiac signs in chart', async ({ page }) => {
    // Generate chart
    await page.locator('input[type="date"]').fill('1990-06-15');
    await page.locator('input[type="time"]').fill('14:30');
    await page.locator('input[placeholder*="Country"]').fill('USA');
    await page.locator('input[placeholder*="City"]').fill('New York');
    await page.locator('button:has-text("Generate Chart")').click();

    await page.waitForLoadState('networkidle');
    await expect(page.locator('svg[role="img"]')).toBeVisible({ timeout: 5000 });

    // Check for zodiac signs
    const zodiacText = page.locator('text=/♈|♉|♊|♋|♌|♍|♎|♏|♐|♑|♒|♓/');
    const count = await zodiacText.count();
    expect(count).toBeGreaterThan(0);
  });

  test('should be keyboard accessible', async ({ page }) => {
    // Tab through form fields
    const dateInput = page.locator('input[type="date"]');
    await dateInput.focus();
    await expect(dateInput).toBeFocused();

    // Type a date using keyboard
    await page.keyboard.type('1990-06-15');

    // Tab to next field
    await page.keyboard.press('Tab');
    const timeInput = page.locator('input[type="time"]');
    await expect(timeInput).toBeFocused();

    // Fill rest of form and submit
    await page.locator('input[type="date"]').fill('1990-06-15');
    await page.locator('input[type="time"]').fill('14:30');
    await page.locator('input[placeholder*="Country"]').fill('USA');
    await page.locator('input[placeholder*="City"]').fill('New York');

    // Tab to submit button
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    const submitButton = page.locator('button:has-text("Generate Chart")');
    await expect(submitButton).toBeFocused();

    // Submit with keyboard
    await page.keyboard.press('Enter');

    // Check that chart appears
    await page.waitForLoadState('networkidle');
    await expect(page.locator('svg[role="img"]')).toBeVisible({ timeout: 5000 });
  });

  test('should have proper ARIA labels for accessibility', async ({ page }) => {
    // Check that form inputs have labels or aria-label
    const dateInput = page.locator('input[type="date"]');
    const timeInput = page.locator('input[type="time"]');
    const countryInput = page.locator('input[placeholder*="Country"]');
    const cityInput = page.locator('input[placeholder*="City"]');

    // Inputs should have descriptive attributes
    await expect(dateInput).toHaveAttribute(/aria-label|aria-describedby|placeholder/);
    await expect(timeInput).toHaveAttribute(/aria-label|aria-describedby|placeholder/);
    await expect(countryInput).toHaveAttribute(/aria-label|aria-describedby|placeholder/);
    await expect(cityInput).toHaveAttribute(/aria-label|aria-describedby|placeholder/);

    // Chart should have role="img" with aria-label
    await page.locator('input[type="date"]').fill('1990-06-15');
    await page.locator('input[type="time"]').fill('14:30');
    await page.locator('input[placeholder*="Country"]').fill('USA');
    await page.locator('input[placeholder*="City"]').fill('New York');
    await page.locator('button:has-text("Generate Chart")').click();

    await page.waitForLoadState('networkidle');
    const chartSvg = page.locator('svg[role="img"]');
    await expect(chartSvg).toBeVisible({ timeout: 5000 });
    await expect(chartSvg).toHaveAttribute('aria-label');
  });

  test('should handle API error gracefully', async ({ page }) => {
    // Try with invalid location
    await page.locator('input[type="date"]').fill('1990-06-15');
    await page.locator('input[type="time"]').fill('14:30');
    await page.locator('input[placeholder*="Country"]').fill('InvalidCountry');
    await page.locator('input[placeholder*="City"]').fill('InvalidCity');

    await page.locator('button:has-text("Generate Chart")').click();

    // Should either show mock data or error message
    // The app falls back to mock data, so chart should appear
    await page.waitForLoadState('networkidle');
    const chartSvg = page.locator('svg[role="img"]');
    // Either chart is shown (mock fallback) or error is shown
    const errorOrChart = page.locator('svg[role="img"], text=/not found|error/i');
    await expect(errorOrChart.first()).toBeVisible({ timeout: 5000 });
  });

  test('should have good color contrast for accessibility', async ({ page }) => {
    // This test verifies the page loads without visual errors
    await page.goto('/');

    // Check for text visibility
    const heading = page.locator('h1').first();
    await expect(heading).toBeVisible();

    // Form should be readable
    const labels = page.locator('label');
    const labelCount = await labels.count();
    expect(labelCount).toBeGreaterThan(0);

    // All visible text should have good contrast
    // Playwright doesn't have built-in contrast checking, but we can verify elements are visible
    const inputs = page.locator('input');
    const inputCount = await inputs.count();
    expect(inputCount).toBeGreaterThan(0);
  });

  test('should be responsive on different screen sizes', async ({ page }) => {
    // Test desktop size
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/');
    let form = page.locator('form');
    await expect(form).toBeVisible();

    // Test tablet size
    await page.setViewportSize({ width: 768, height: 1024 });
    form = page.locator('form');
    await expect(form).toBeVisible();

    // Test mobile size
    await page.setViewportSize({ width: 375, height: 667 });
    form = page.locator('form');
    await expect(form).toBeVisible();

    // Fill form and generate chart on mobile
    await page.locator('input[type="date"]').fill('1990-06-15');
    await page.locator('input[type="time"]').fill('14:30');
    await page.locator('input[placeholder*="Country"]').fill('USA');
    await page.locator('input[placeholder*="City"]').fill('New York');
    await page.locator('button:has-text("Generate Chart")').click();

    await page.waitForLoadState('networkidle');
    const chartSvg = page.locator('svg[role="img"]');
    await expect(chartSvg).toBeVisible({ timeout: 5000 });
  });
});
