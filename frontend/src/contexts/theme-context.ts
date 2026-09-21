import {
    createContext,
    useContext,
} from "react"


export type Theme =
    | "dark"
    | "light"
    | "system"


export type ThemeProviderState = {
    theme: Theme
    setTheme: (
        theme: Theme
    ) => void
}


const initialState:
    ThemeProviderState = {

    theme: "system",

    setTheme: () => undefined,

}


export const ThemeProviderContext =
    createContext<ThemeProviderState>(
        initialState
    )


export function useTheme() {

    return useContext(
        ThemeProviderContext
    )

}