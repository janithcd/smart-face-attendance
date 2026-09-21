import js from "@eslint/js"
import globals from "globals"

import reactHooks from "eslint-plugin-react-hooks"
import reactRefresh from "eslint-plugin-react-refresh"

import pluginQuery from "@tanstack/eslint-plugin-query"

import tseslint from "typescript-eslint"

import {
  defineConfig,
  globalIgnores,
} from "eslint/config"


export default defineConfig([

  globalIgnores([
    "dist",
  ]),

  ...pluginQuery.configs[
      "flat/recommended"
      ],

  {
    files: [
      "**/*.{ts,tsx}",
    ],

    extends: [
      js.configs.recommended,
      tseslint.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],

    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
    },
  },


  // shadcn/ui generated components
  // intentionally export helpers together
  // with React components.
  {
    files: [
      "src/components/ui/**/*.{ts,tsx}",
    ],

    rules: {
      "react-refresh/only-export-components":
          "off",
    },
  },

])