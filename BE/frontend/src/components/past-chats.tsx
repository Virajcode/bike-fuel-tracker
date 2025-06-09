"use client";

import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { MessageCircle, PanelLeftClose, PanelLeftOpen } from "lucide-react";
import { cn } from "@/lib/utils";

interface PastChatsProps {
  isCollapsed: boolean;
  onToggle: () => void;
}

export function PastChats({ isCollapsed, onToggle }: PastChatsProps) {
  // Mock data for chat history - TODO: Replace with real data
  const mockChats = [
    { id: "1", title: "Best Hotels in pune", date: "2h ago" },
    { id: "2", title: "Trip plan to goa", date: "5h ago" },
    { id: "3", title: "Family dinner in katraj", date: "Yesterday" },
    { id: "4", title: "Packing list for trek", date: "2 days ago" },
  ];

  return (
    <div className={cn(
      "flex flex-col h-full transition-all duration-300 ease-in-out",
      isCollapsed ? "w-16" : "w-64"
    )}>
      <div className="p-2 border-b flex justify-between items-center">
        <h2 className={cn(
          "font-semibold transition-opacity text-sm flex-1",
          isCollapsed ? "hidden" : "block"
        )}>
          Chat History
        </h2>
        <Button
          variant="ghost"
          size="sm"
          className="h-8 w-8"
          onClick={onToggle}
        >
          {isCollapsed ? (
            <PanelLeftOpen className="h-4 w-4" />
          ) : (
            <PanelLeftClose className="h-4 w-4" />
          )}
          <span className="sr-only">
            {isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
          </span>
        </Button>
      </div>
      <ScrollArea className="flex-grow">
        <div className={cn("space-y-1 p-2")}>
          {mockChats.map((chat) => (
            <Button
              key={chat.id}
              variant="ghost"
              className={cn(
                "w-full h-10",
                isCollapsed ? "justify-center px-2" : "justify-start px-3"
              )}
              title={isCollapsed ? chat.title : undefined}
            >
              <MessageCircle className="h-4 w-4 shrink-0" />
              {!isCollapsed && (
                <div className="ml-2 flex flex-col items-start text-sm overflow-hidden">
                  <span className="font-medium truncate w-full">{chat.title}</span>
                  <span className="text-xs text-muted-foreground">{chat.date}</span>
                </div>
              )}
            </Button>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}
