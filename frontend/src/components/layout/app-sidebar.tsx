import {
    Activity,
    ChevronsUpDown,
    LogOut,
    Shield,
    User,
} from "lucide-react"

import {
    Link,
    useLocation,
} from "react-router"

import {
    mainNavigation,
    systemNavigation,
} from "@/config/navigation"

import {
    Avatar,
    AvatarFallback,
} from "@/components/ui/avatar"

import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarGroup,
    SidebarGroupContent,
    SidebarGroupLabel,
    SidebarHeader,
    SidebarMenu,
    SidebarMenuButton,
    SidebarMenuItem,
    SidebarRail,
    useSidebar,
} from "@/components/ui/sidebar"


export function AppSidebar() {

    const location =
        useLocation()

    const {
        isMobile,
        setOpenMobile,
    } = useSidebar()


    function isRouteActive(
        href: string
    ) {

        if (href === "/") {
            return location.pathname === "/"
        }

        return (
            location.pathname === href ||
            location.pathname.startsWith(
                `${href}/`
            )
        )
    }


    function closeMobileSidebar() {

        if (isMobile) {
            setOpenMobile(false)
        }

    }


    return (

        <Sidebar
            collapsible="icon"
        >

            <SidebarHeader>

                <SidebarMenu>

                    <SidebarMenuItem>

                        <SidebarMenuButton
                            size="lg"
                            tooltip="Smart Attendance"
                            render={
                                <Link
                                    to="/"
                                    onClick={
                                        closeMobileSidebar
                                    }
                                />
                            }
                        >

                            <div
                                className="
                  flex
                  size-8
                  items-center
                  justify-center
                  rounded-lg
                  bg-primary
                  text-primary-foreground
                "
                            >
                                <Activity
                                    className="size-4"
                                />
                            </div>


                            <div
                                className="
                  grid
                  flex-1
                  text-left
                  text-sm
                  leading-tight
                "
                            >

                <span
                    className="
                    truncate
                    font-semibold
                  "
                >
                  Smart Attendance
                </span>

                                <span
                                    className="
                    truncate
                    text-xs
                    text-muted-foreground
                  "
                                >
                  Biometric Platform
                </span>

                            </div>

                        </SidebarMenuButton>

                    </SidebarMenuItem>

                </SidebarMenu>

            </SidebarHeader>


            <SidebarContent>

                <SidebarGroup>

                    <SidebarGroupLabel>
                        Platform
                    </SidebarGroupLabel>

                    <SidebarGroupContent>

                        <SidebarMenu>

                            {mainNavigation.map(
                                (item) => {

                                    const Icon =
                                        item.icon

                                    return (

                                        <SidebarMenuItem
                                            key={item.href}
                                        >

                                            <SidebarMenuButton
                                                tooltip={item.title}
                                                isActive={
                                                    isRouteActive(
                                                        item.href
                                                    )
                                                }
                                                render={
                                                    <Link
                                                        to={item.href}
                                                        onClick={
                                                            closeMobileSidebar
                                                        }
                                                    />
                                                }
                                            >

                                                <Icon />

                                                <span>
                          {item.title}
                        </span>

                                            </SidebarMenuButton>

                                        </SidebarMenuItem>

                                    )

                                }
                            )}

                        </SidebarMenu>

                    </SidebarGroupContent>

                </SidebarGroup>


                <SidebarGroup>

                    <SidebarGroupLabel>
                        System
                    </SidebarGroupLabel>

                    <SidebarGroupContent>

                        <SidebarMenu>

                            {systemNavigation.map(
                                (item) => {

                                    const Icon =
                                        item.icon

                                    return (

                                        <SidebarMenuItem
                                            key={item.href}
                                        >

                                            <SidebarMenuButton
                                                tooltip={item.title}
                                                isActive={
                                                    isRouteActive(
                                                        item.href
                                                    )
                                                }
                                                render={
                                                    <Link
                                                        to={item.href}
                                                        onClick={
                                                            closeMobileSidebar
                                                        }
                                                    />
                                                }
                                            >

                                                <Icon />

                                                <span>
                          {item.title}
                        </span>

                                            </SidebarMenuButton>

                                        </SidebarMenuItem>

                                    )

                                }
                            )}

                        </SidebarMenu>

                    </SidebarGroupContent>

                </SidebarGroup>

            </SidebarContent>


            <SidebarFooter>

                <SidebarMenu>

                    <SidebarMenuItem>

                        <DropdownMenu>

                            <DropdownMenuTrigger
                                render={
                                    <SidebarMenuButton
                                        size="lg"
                                        tooltip="Administrator"
                                    />
                                }
                            >

                                <Avatar
                                    size="sm"
                                >

                                    <AvatarFallback>
                                        AD
                                    </AvatarFallback>

                                </Avatar>


                                <div
                                    className="
                    grid
                    flex-1
                    text-left
                    text-sm
                    leading-tight
                  "
                                >

                  <span
                      className="
                      truncate
                      font-medium
                    "
                  >
                    Administrator
                  </span>

                                    <span
                                        className="
                      truncate
                      text-xs
                      text-muted-foreground
                    "
                                    >
                    Local development
                  </span>

                                </div>


                                <ChevronsUpDown
                                    className="ml-auto"
                                />

                            </DropdownMenuTrigger>


                            <DropdownMenuContent
                                side="top"
                                align="start"
                                className="w-56"
                            >

                                <DropdownMenuLabel>
                                    Account
                                </DropdownMenuLabel>

                                <DropdownMenuSeparator />


                                <DropdownMenuItem>
                                    <User />
                                    Profile
                                </DropdownMenuItem>


                                <DropdownMenuItem>
                                    <Shield />
                                    Security
                                </DropdownMenuItem>


                                <DropdownMenuSeparator />


                                <DropdownMenuItem
                                    variant="destructive"
                                >
                                    <LogOut />
                                    Sign out
                                </DropdownMenuItem>

                            </DropdownMenuContent>

                        </DropdownMenu>

                    </SidebarMenuItem>

                </SidebarMenu>

            </SidebarFooter>


            <SidebarRail />

        </Sidebar>

    )
}