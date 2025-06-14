"use client";

import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { MessageCircle, PanelLeftClose, PanelLeftOpen, Plus } from "lucide-react";
import { cn } from "@/lib/utils";
import { apiClient } from "@/lib/api-client";
import useSWR from "swr";
import { useRouter } from 'next/navigation';
import { toast } from "sonner";
import type { ChatSession } from "@/lib/api-client";

interface PastChatsProps {
  isCollapsed: boolean;
  onToggle: () => void;
}

export function PastChats({ isCollapsed, onToggle }: PastChatsProps) {
  const router = useRouter();
  const { data: sessions, error, mutate } = useSWR('/chat/sessions', apiClient.chat.getSessions);

  const formatDate = (date: string) => {
    const d = new Date(date);
    const now = new Date();
    const diff = now.getTime() - d.getTime();
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor(diff / (1000 * 60 * 60));

    if (days > 1) return `${days} days ago`;
    if (days === 1) return 'Yesterday';
    if (hours > 0) return `${hours}h ago`;
    return 'Just now';
  };

  const handleCreateNewChat = async () => {
    try {
      const newSession = await apiClient.chat.createSession("New Chat");
      localStorage.setItem("selectedSessionId", newSession.toString());
      window.location.reload();
      router.push(`/dashboard`);
      mutate(); // Refresh the sessions list
    } catch (error) {
      console.error('Failed to create new chat:', error);
      toast.error("Failed to create new chat session");
    }
  };

  const handleSessionClick = (sessionId: number) => {
    localStorage.setItem("selectedSessionId", sessionId.toString());
      window.location.reload();
    router.push(`/dashboard`);
  };

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
          {error && (
            <div className="text-sm text-red-500 p-2">Failed to load chat sessions</div>
          )}
          {!sessions && !error && (
            <div className="text-sm text-gray-500 p-2">Loading sessions...</div>
          )}
          {sessions && sessions.length === 0 && (
            <div className="text-sm text-gray-500 p-2">No chat sessions yet</div>
          )}
          {sessions?.map((session: ChatSession) => (
            <Button
              key={session.id}
              variant="ghost"
              className={cn(
                "w-full justify-start gap-2",
                isCollapsed ? "px-2" : "px-4"
              )}
              onClick={() => handleSessionClick(session.id)}
            >
              <MessageCircle className="h-4 w-4" />
              {!isCollapsed && (
                <>
                  <span className="flex-1 truncate text-sm">
                    {session.topic || "New Chat"}
                  </span>
                  <span className="text-xs text-gray-400">
                    {formatDate(session.last_updated)}
                  </span>
                </>
              )}
            </Button>
          ))}
        </div>
      </ScrollArea>
      <div className="p-2 border-t">
        <Button
          variant="outline"
          className={cn(
            "w-full justify-start gap-2",
            isCollapsed ? "px-2" : "px-4"
          )}
          onClick={handleCreateNewChat}
        >
          <Plus className="h-4 w-4" />
          {!isCollapsed && (
            <span className="flex-1 text-sm">New Chat</span>
          )}
        </Button>
      </div>
    </div>
  );
}
