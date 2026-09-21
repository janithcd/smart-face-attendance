import {
    useEffect,
    useState,
    type ReactNode,
} from "react"

import {
    ThemeProviderContext,
    type Theme,
} from "@/contexts/theme-context"


type ThemeProviderProps = {
    children: ReactNode
    defaultTheme?: Theme
    storageKey?: string
}


const SYSTEM_THEME_QUERY =
    "(prefers-color-scheme: dark)"


export function ThemeProvider({
                                  children,
                                  defaultTheme = "system",
                                  storageKey = "smart-attendance-theme",
                              }: ThemeProviderProps) {

    const [
        theme,
        setThemeState,
    ] = useState<Theme>(() => {

        const storedTheme =
            localStorage.getItem(
                storageKey
            ) as Theme | null

        return storedTheme ?? defaultTheme
    })


    useEffect(() => {

        const root =
            window.document.documentElement

        const mediaQuery =
            window.matchMedia(
                SYSTEM_THEME_QUERY
            )


        const applyTheme = () => {

            root.classList.remove(
                "light",
                "dark"
            )

            const resolvedTheme =
                theme === "system"
                    ? mediaQuery.matches
                        ? "dark"
                        : "light"
                    : theme

            root.classList.add(
                resolvedTheme
            )
        }


        applyTheme()


        if (theme !== "system") {
            return
        }


        mediaQuery.addEventListener(
            "change",
            applyTheme
        )


        return () => {

            mediaQuery.removeEventListener(
                "change",
                applyTheme
            )

        }

    }, [theme])


    function setTheme(
        newTheme: Theme
    ) {

        localStorage.setItem(
            storageKey,
            newTheme
        )

        setThemeState(
            newTheme
        )
    }


    return (

        <ThemeProviderContext.Provider
            value={{
                theme,
                setTheme,
            }}
        >

            {children}

        </ThemeProviderContext.Provider>

    )
}