// 1. Import utilities from `astro:content`
import { z, defineCollection } from "astro:content"

const blogCollection = defineCollection({
  type: "content", // v2.5.0 and later
  schema: z.object({
    title: z.string(),
    author: z.string(),
    tags: z.array(z.string()).optional(),
    imageUri: z.string().optional(),
    published: z.string().transform((str) => new Date(str)),
    introContent: z.string().optional(),
    summary: z.string(),
    readingTime: z.number().optional(),
    recommendations: z
      .array(
        z.object({
          slug: z.string(),
          title: z.string(),
        })
      )
      .optional(),
    qaSection: z
      .array(
        z.object({
          question: z.string(),
          answer: z.string(),
        })
      )
      .optional(),
  }),
})

// 3. Export a single `collections` object to register your collection(s)
export const collections = {
  blog: blogCollection,
}
