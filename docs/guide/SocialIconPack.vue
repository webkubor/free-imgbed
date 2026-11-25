<script setup lang="ts">
import { ref } from 'vue'
import { withBase } from 'vitepress'
import pack from '../../social-icons/pack-v2.json'

type Icon = { name: string; file: string; colorFile?: string; brandColors: string[] }
type Style = 'brand' | 'mono'
const iconBase = 'https://imgbed.webkubor.online/social-icons/'
const download = withBase(`/downloads/social-icons-v${pack.version}.zip`)
const style = ref<Style>('brand')
const copyStatus = ref('')
const copied = ref('')
const manualLink = ref('')
const iconUrl = (file: string) => iconBase + file
const shownFile = (icon: Icon) => style.value === 'brand' ? icon.colorFile ?? icon.file : icon.file

function selectStyle(next: Style) {
  style.value = next
  copied.value = ''
  manualLink.value = ''
  copyStatus.value = ''
}

async function copyLink(icon: Icon) {
  const file = shownFile(icon)
  const url = iconUrl(file)
  try {
    await navigator.clipboard.writeText(url)
    copied.value = file
    manualLink.value = ''
    copyStatus.value = `已复制 ${icon.name} 的直链`
  } catch {
    copied.value = ''
    copyStatus.value = ''
    manualLink.value = url
  }
}
</script>

<template>
  <p><a :href="download" download>下载 ZIP 图标包（含品牌色与单色）</a></p>
  <div class="icon-actions icon-mode" role="group" aria-label="图标配色">
    <button type="button" :aria-pressed="style === 'brand'" @click="selectStyle('brand')">品牌色</button>
    <button type="button" :aria-pressed="style === 'mono'" @click="selectStyle('mono')">单色 SVG</button>
  </div>
  <p v-if="manualLink" role="status">
    请手动复制 <input :value="manualLink" readonly aria-label="图标直链" @focus="($event.target as HTMLInputElement).select()">
  </p>
  <span class="copy-status" role="status">{{ copyStatus }}</span>

  <section v-for="group in pack.groups" :key="group.name">
    <h2>{{ group.name }}</h2>
    <ul class="icon-grid">
      <li v-for="icon in group.icons" :key="icon.file" class="icon-card">
        <img :src="iconUrl(shownFile(icon))" class="icon-preview" width="40" height="40" alt="">
        <strong>{{ icon.name }}</strong>
        <div class="brand-colors" :aria-label="`${icon.name} 品牌色`">
          <code v-for="color in icon.brandColors" :key="color" :style="{ '--swatch': color }">{{ color }}</code>
        </div>
        <div class="icon-actions">
          <a :href="iconUrl(shownFile(icon))" :aria-label="`打开 ${icon.name} 图标`">{{ icon.file.endsWith('.svg') ? 'SVG' : 'PNG' }}</a>
          <button type="button" :aria-label="`复制 ${icon.name} 图标直链`" @click="copyLink(icon)">
            {{ copied === shownFile(icon) ? '已复制' : '复制直链' }}
          </button>
        </div>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.icon-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(9rem, 1fr));
  gap: 0.75rem;
  padding: 0;
  list-style: none;
}

.icon-card {
  display: grid;
  justify-items: start;
  gap: 0.5rem;
  margin: 0;
  padding: 0.75rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.5rem;
  background: var(--vp-c-bg-soft);
}

.icon-preview {
  box-sizing: border-box;
  padding: 0.5rem;
  object-fit: contain;
  border-radius: 0.5rem;
  background: var(--vp-c-white);
}

.icon-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.icon-actions button {
  border: 1px solid var(--vp-c-divider);
  border-radius: 0.25rem;
  padding: 0 0.375rem;
  background: var(--vp-c-bg);
}

.icon-actions button:focus-visible {
  outline: 2px solid var(--vp-c-brand-1);
}

.icon-mode button {
  padding: 0.25rem 0.625rem;
}

.icon-mode button[aria-pressed='true'] {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}

.brand-colors {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.brand-colors code {
  padding: 0.125rem 0.25rem;
  font-size: 0.75rem;
  color: var(--vp-c-text-2);
}

.brand-colors code::before {
  display: inline-block;
  width: 0.5rem;
  height: 0.5rem;
  margin-right: 0.25rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 50%;
  background: var(--swatch);
  content: '';
}

.copy-status {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
}
</style>
