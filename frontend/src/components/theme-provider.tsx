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


export function ThemeProvider({
                                  children,
                                  defaultTheme = "system",
                                  storageKey =
                                  "smart-attendance-theme",
                              }: ThemeProviderProps) {

    const [
        theme,
        setThemeState,
    ] = useState<Theme>(() => {

        const storedTheme =
            localStorage.getItem(
                storageKey
            ) as Theme | null

        return (
            storedTheme ??
            defaultTheme
        )
    })


    useEffect(() => {

        const root =
            window.document.documentElement

        root.classList.remove(
            "light",
            "dark"
        )


        if (theme === "system") {

            const systemTheme =
                window.matchMedia(
                    "(prefers-color-scheme: dark)"
                ).matches
                    ? "dark"
                    : "light"

            root.classList.add(
                systemTheme
            )

            return
        }


        root.classList.add(
            theme
        )

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