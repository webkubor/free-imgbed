import DefaultTheme from 'vitepress/theme'
import { onMounted } from 'vue'
import { trackPageView } from './analytics.js'

export default {
  extends: DefaultTheme,
  enhanceApp({ router }) {
    router.onAfterRouteChanged = () => trackPageView()
  },
  setup() { onMounted(() => trackPageView()) },
}
