import { defineConfig, sharpImageService } from "astro/config"
import tailwind from "@astrojs/tailwind"
import solidJs from "@astrojs/solid-js"
import mdx from "@astrojs/mdx"

// https://astro.build/config
export default defineConfig({
  site: "https://some-example-site.com",
  image: {
    service: sharpImageService(),
  },
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },
  output: "server",
  integrations: [tailwind(), solidJs(), mdx()],
})
