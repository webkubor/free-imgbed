import { readFile } from 'node:fs/promises'
import { expect, test, type Page } from '@playwright/test'
import pack from '../../social-icons/pack-v3.json' with { type: 'json' }

const guide = '/guide/social-icons.html'
const iconBase = 'https://imgbed.webkubor.online/social-icons/'
const zip = `/downloads/social-icons-v${pack.version}.zip`
const total = pack.groups.flatMap(group => group.icons).length

test.beforeEach(async ({ context, baseURL }) => {
  // Use the built image mirror so unpublished changes are checked without production cache.
  await context.route(`${iconBase}**`, async route => {
    const source = new URL(route.request().url())
    const response = await route.fetch({ url: new URL(source.pathname, baseURL).href })
    await route.fulfill({ response })
  })
})

async function expectLoadedIcons(page: Page, count = total) {
  const icons = page.locator('.icon-preview')
  await expect(icons).toHaveCount(count)
  await expect.poll(() => icons.evaluateAll(images =>
    images.every(image => image instanceof HTMLImageElement && image.complete && image.naturalWidth > 0),
  )).toBe(true)
}

test('desktop: brand icons, palette, clipboard, and ZIP', async ({ page, context }, testInfo) => {
  await page.setViewportSize({ width: 1440, height: 900 })
  await page.emulateMedia({ colorScheme: 'light' })
  await context.grantPermissions(['clipboard-read', 'clipboard-write'])
  await page.goto('/')
  await page.getByRole('link', { name: '浏览图标包', exact: true }).click()
  await expect(page).toHaveURL(new RegExp(`${guide}$`))
  await expectLoadedIcons(page)

  const payment = page.getByRole('navigation', { name: '图标分类' })
    .getByRole('link', { name: '支付与购物' })
  await payment.click()
  await expect(page).toHaveURL(/#payment$/)
  await expect(page.locator('#payment').getByText('支付宝', { exact: true })).toBeVisible()
  const search = page.getByRole('searchbox', { name: '搜索图标' })
  await search.fill('掘金')
  await expectLoadedIcons(page, 1)
  await expect(page.getByRole('link', { name: '打开 掘金 图标' }))
    .toHaveAttribute('href', `${iconBase}color/juejin.svg`)
  await expect(page.getByText('#007FFF', { exact: true })).toBeVisible()
  await search.fill('支付宝')
  await expectLoadedIcons(page, 1)
  await search.fill('ALIPAY')
  await expectLoadedIcons(page, 1)
  await expect(page.getByRole('link', { name: '打开 支付宝 图标' }))
    .toHaveAttribute('href', `${iconBase}color/alipay.svg`)
  await expect(page.getByText('#1677FF', { exact: true })).toBeVisible()
  await search.fill('no-platform-matches')
  await expect(page.getByText('没有找到匹配的图标。', { exact: false })).toBeVisible()
  await search.fill('')
  await expectLoadedIcons(page)

  const brand = page.getByRole('button', { name: '品牌色', exact: true })
  const discord = page.getByRole('link', { name: '打开 Discord 图标', exact: true })
  await expect(brand).toHaveAttribute('aria-pressed', 'true')
  await expect(page.getByRole('link', { name: '打开 Google 图标', exact: true }))
    .toHaveAttribute('href', `${iconBase}color/google.svg`)
  for (const hex of ['#4285F4', '#EA4335', '#FBBC05', '#34A853', '#181717', '#5865F2']) {
    await expect(page.getByText(hex, { exact: true })).toBeVisible()
  }
  await expect(discord).toHaveAttribute('href', `${iconBase}color/discord.svg`)
  await page.getByRole('button', { name: '单色 SVG', exact: true }).click()
  await expect(discord).toHaveAttribute('href', `${iconBase}discord.svg`)
  await brand.click()
  await expect(discord).toHaveAttribute('href', `${iconBase}color/discord.svg`)
  await expectLoadedIcons(page)

  const lineup = await page.locator('.icon-card').evaluateAll(cards => {
    const firstRow = ['Google', 'GitHub', 'Discord', 'X（推特）']
      .map(name => cards.find(card => card.querySelector('strong')?.textContent === name))
    return firstRow.map(card => ({
      title: card?.querySelector('strong')?.getBoundingClientRect().top,
      actions: card?.querySelector('.icon-actions')?.getBoundingClientRect().top,
    }))
  })
  expect(lineup.every(card => typeof card.title === 'number' && typeof card.actions === 'number')).toBe(true)
  for (const card of lineup.slice(1)) {
    expect(card.title).toBeCloseTo(lineup[0].title ?? -1, 0)
    expect(card.actions).toBeCloseTo(lineup[0].actions ?? -1, 0)
  }

  const copy = page.getByRole('button', { name: '复制 Discord 图标直链', exact: true })
  await copy.click()
  await expect(copy).toHaveText('已复制')
  await expect.poll(() => page.evaluate(() => navigator.clipboard.readText()))
    .toBe(`${iconBase}color/discord.svg`)

  const downloadPromise = page.waitForEvent('download')
  await page.getByRole('link', { name: /下载 ZIP 图标包/ }).click()
  const download = await downloadPromise
  expect(new URL(download.url()).pathname).toBe(zip)
  expect(await download.failure()).toBeNull()
  const bytes = await readFile(await download.path())
  expect(bytes.equals(await readFile(new URL(`../.vitepress/dist${zip}`, import.meta.url)))).toBe(true)
  await page.screenshot({ path: testInfo.outputPath('desktop.png'), fullPage: true, animations: 'disabled' })
})

test('mobile: dark mode and no horizontal overflow', async ({ page }, testInfo) => {
  await page.setViewportSize({ width: 390, height: 844 })
  await page.emulateMedia({ colorScheme: 'dark' })
  await page.goto(guide)
  await expect(page.locator('html')).toHaveClass(/\bdark\b/)
  await expectLoadedIcons(page)
  expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBe(390)
  await page.screenshot({ path: testInfo.outputPath('mobile-dark.png'), fullPage: true, animations: 'disabled' })
})
