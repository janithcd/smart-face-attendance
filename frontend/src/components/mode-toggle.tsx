import {
    Laptop,
    Moon,
    Sun,
} from "lucide-react"

import {
    useTheme,
} from "@/contexts/theme-context"

import {
    Button,
} from "@/components/ui/button"

import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"


export function ModeToggle() {

    const {
        setTheme,
    } = useTheme()

    return (
        <DropdownMenu>

            <DropdownMenuTrigger
                render={
                    <Button
                        variant="outline"
                        size="icon"
                        aria-label="Change theme"
                    />
                }
            >

                <Sun
                    className="
            h-[1.2rem]
            w-[1.2rem]
            scale-100
            rotate-0
            transition-all
            dark:scale-0
            dark:-rotate-90
          "
                />

                <Moon
                    className="
            absolute
            h-[1.2rem]
            w-[1.2rem]
            scale-0
            rotate-90
            transition-all
            dark:scale-100
            dark:rotate-0
          "
                />

                <span className="sr-only">
          Change theme
        </span>

            </DropdownMenuTrigger>


            <DropdownMenuContent
                align="end"
            >

                <DropdownMenuItem
                    onClick={() =>
                        setTheme("light")
                    }
                >
                    <Sun />
                    Light
                </DropdownMenuItem>


                <DropdownMenuItem
                    onClick={() =>
                        setTheme("dark")
                    }
                >
                    <Moon />
                    Dark
                </DropdownMenuItem>


                <DropdownMenuItem
                    onClick={() =>
                        setTheme("system")
                    }
                >
                    <Laptop />
                    System
                </DropdownMenuItem>

            </DropdownMenuContent>

        </DropdownMenu>
    )
}