'use client';

import { Chat } from "@/components/chat";
import { generateUUID } from "@/lib/utils";
import { PastChats } from "@/components/past-chats";
import { useState } from "react";
import { cn } from "@/lib/utils";

export default function Home() {
  const id = generateUUID();
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);

  return (
    <div className="flex h-[calc(100vh-56px)] mt-14">
      <aside className={cn(
        "border-r border-border bg-muted/40 min-h-full",
        "transition-[width] duration-300 ease-in-out overflow-hidden",
        isSidebarCollapsed ? "w-16" : "w-64"
      )}>
        <PastChats 
          isCollapsed={isSidebarCollapsed} 
          onToggle={() => setIsSidebarCollapsed(!isSidebarCollapsed)} 
        />
      </aside>
      <div className="flex-grow">
        <Chat id={id} />
      </div>
    </div>
  );
}