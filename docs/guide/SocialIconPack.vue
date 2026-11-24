<script setup lang="ts">
import { ref } from 'vue'
import { withBase } from 'vitepress'
import pack from '../../social-icons/pack.json'

const iconBase = 'https://cdn.jsdelivr.net/gh/webkubor/free-imgbed@main/social-icons/'
const download = withBase(`/downloads/social-icons-v${pack.version}.zip`)
const copyStatus = ref('')
const copied = ref('')
const manualLink = ref('')
const iconUrl = (file: string) => iconBase + file

async function copyLink(icon: { name: string; file: string }) {
  const url = iconUrl(icon.file)
  try {
    await navigator.clipboard.writeText(url)
    copied.value = icon.file
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
  <p><a :href="download" download>下载 ZIP 图标包</a></p>
  <p v-if="manualLink" role="status">
    请手动复制 <input :value="manualLink" readonly aria-label="图标直链" @focus="($event.target as HTMLInputElement).select()">
  </p>
  <span class="copy-status" role="status">{{ copyStatus }}</span>

  <section v-for="group in pack.groups" :key="group.name">
    <h2>{{ group.name }}</h2>
    <ul class="icon-grid">
      <li v-for="icon in group.icons" :key="icon.file" class="icon-card">
        <img :src="iconUrl(icon.file)" class="icon-preview" width="40" height="40" alt="">
        <strong>{{ icon.name }}</strong>
        <div class="icon-actions">
          <a :href="iconUrl(icon.file)" :aria-label="`打开 ${icon.name} 原图`">{{ icon.file.endsWith('.svg') ? 'SVG' : 'PNG' }}</a>
          <button type="button" :aria-label="`复制 ${icon.name} 图标直链`" @click="copyLink(icon)">
            {{ copied === icon.file ? '已复制' : '复制直链' }}
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

.copy-status {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
}
</style>
