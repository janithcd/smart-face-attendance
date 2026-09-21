import type {
    LucideIcon,
} from "lucide-react"

import {
    BarChart,
    LayoutDashboard,
    Monitor,
    Plug,
    ScanFace,
    Settings,
    Users,
} from "lucide-react"


export type NavigationItem = {
    title: string
    href: string
    icon: LucideIcon
}


export const mainNavigation:
    NavigationItem[] = [

    {
        title: "Dashboard",
        href: "/",
        icon: LayoutDashboard,
    },

    {
        title: "Attendance",
        href: "/attendance",
        icon: ScanFace,
    },

    {
        title: "People",
        href: "/people",
        icon: Users,
    },

    {
        title: "Devices",
        href: "/devices",
        icon: Monitor,
    },

    {
        title: "Reports",
        href: "/reports",
        icon: BarChart,
    },

    {
        title: "Integrations",
        href: "/integrations",
        icon: Plug,
    },

]


export const systemNavigation:
    NavigationItem[] = [

    {
        title: "Settings",
        href: "/settings",
        icon: Settings,
    },

]


export function getPageTitle(
    pathname: string
) {

    const navigation = [
        ...mainNavigation,
        ...systemNavigation,
    ]


    const exactMatch =
        navigation.find(
            (item) =>
                item.href === pathname
        )


    if (exactMatch) {
        return exactMatch.title
    }


    const nestedMatch =
        navigation.find(
            (item) =>
                item.href !== "/" &&
                pathname.startsWith(
                    `${item.href}/`
                )
        )


    return (
        nestedMatch?.title ??
        "Smart Attendance"
    )
}