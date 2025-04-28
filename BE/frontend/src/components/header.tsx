'use client'

import React from 'react'
import { HomeIcon, Settings2 } from 'lucide-react'
import Link from 'next/link'

export const Header: React.FC = () => {
  return (
    <header className="fixed top-0 w-full z-20 bg-white/70 dark:bg-black/30 backdrop-blur-md border-b border-border px-4 py-2 flex items-center justify-between">
      {/* Left: Logo / Home */}
      <Link href="/" className="flex items-center gap-2 text-foreground hover:opacity-80 transition-opacity">
        <HomeIcon size={20} />
        <span className="text-sm font-medium hidden sm:inline">Location Chat</span>
      </Link>

      {/* Right: Settings / Profile */}
      <div className="flex items-center gap-3">
        <button className="p-2 rounded-full hover:bg-muted transition-colors">
          <Settings2 size={18} />
          <span className="sr-only">Settings</span>
        </button>
        {/* You can add avatar or menu here later */}
      </div>
    </header>
  )
}

export default Header
