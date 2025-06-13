'use client';

import { Chat } from "@/components/chat";
import { generateUUID } from "@/lib/utils";
import { PastChats } from "@/components/past-chats";
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import { SuggestedActions } from "@/components/suggested-actions";


export default function Home() {
  const id = generateUUID();
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);

  // Only set selectedSessionId on first render
  useEffect(() => {
    const storedId = localStorage.getItem("selectedSessionId");
    setSelectedSessionId(storedId);
    console.log("Selected session ID on mount:", storedId);
  }, []);

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
        {selectedSessionId? (
          <Chat/>
        ) : (
          <SuggestedActions />
        )}
      </div>
    </div>
  );
}