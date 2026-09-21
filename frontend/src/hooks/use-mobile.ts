import {
  useSyncExternalStore,
} from "react"


const MOBILE_BREAKPOINT = 768


const mobileQuery =
    `(max-width: ${
        MOBILE_BREAKPOINT - 1
    }px)`


function subscribe(
    callback: () => void
) {

  const mediaQuery =
      window.matchMedia(
          mobileQuery
      )


  const listener = () => {
    callback()
  }


  mediaQuery.addEventListener(
      "change",
      listener
  )


  return () => {

    mediaQuery.removeEventListener(
        "change",
        listener
    )

  }
}


function getSnapshot() {

  return window.matchMedia(
      mobileQuery
  ).matches
}


function getServerSnapshot() {

  return false
}


export function useIsMobile() {

  return useSyncExternalStore(
      subscribe,
      getSnapshot,
      getServerSnapshot
  )
}