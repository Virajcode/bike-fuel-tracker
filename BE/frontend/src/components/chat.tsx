"use client";

import { useEffect, useState, useMemo } from "react";
import { apiClient, ChatMessage } from "@/lib/api-client";
import ChatMessageUI from "./chat-message";
import { ChatInput } from "./chat-input";
import { Message } from "@/lib/types";
import { toast } from "sonner";
import { streamChat } from "@/lib/clients/streamChatClient";

export function Chat() {
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(true);
  const [inputContent, setInputContent] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function fetchHistory() {
      try {
        const sessionId =
          typeof window !== "undefined"
            ? localStorage.getItem("selectedSessionId")
            : null;
        if (!sessionId) return;
        const history = await apiClient.chat.getHistory(parseInt(sessionId));
        setChatHistory(history);
      } catch (err) {
        setChatHistory([]);
      } finally {
        setLoading(false);
      }
    }
    fetchHistory();
  }, []);

  // Convert chat history to user/assistant message pairs
  const messages = useMemo(
    () =>
      chatHistory?.flatMap((msg) => [
        {
          id: msg.id.toString(),
          content: msg.message,
          role: "user" as const,
          createdAt: new Date(msg.timestamp),
        },
        {
          id: `${msg.id}-response`,
          content: msg.response,
          role: "assistant" as const,
          createdAt: new Date(msg.timestamp),
        },
      ]) || [],
    [chatHistory]
  );

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputContent(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!inputContent.trim()) return;
    try {
      setIsLoading(true);
      const sessionId =
        typeof window !== "undefined"
          ? localStorage.getItem("selectedSessionId")
          : null;
      if (!sessionId) return;
      // Save user message
      await apiClient.chat.saveMessage(
        parseInt(sessionId),
        inputContent,
        "",
        "text"
      );
      // Use streamChat to get AI response and append to chat
      await streamChat({
        inputContent,
        setIsLoading,
        append: async (aiMessage) => {
          let aiContent = aiMessage.content;
          let locations = undefined;
          let responseType = "text";
          // Try to parse JSON array for locations
          try {
            const parsed = JSON.parse(aiContent);
            if (Array.isArray(parsed) && parsed[0]?.place_id) {
              locations = parsed;
              aiContent = "Here are some places based on your description:";
              responseType = "json";
            }
          } catch {}
          await apiClient.chat.saveMessage(
            parseInt(sessionId),
            inputContent,
            locations ? JSON.stringify(locations) : aiContent,
            responseType
          );
          // Refresh chat history
          const history = await apiClient.chat.getHistory(parseInt(sessionId));
          setChatHistory(history);
        },
      });
      setInputContent("");
    } catch (error) {
      toast.error("Failed to send message");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col w-full max-w-3xl pt-14 pb-10 mx-auto stretch">
      <ChatMessageUI isLoading={loading || isLoading} messages={messages} />
      <ChatInput
        chatId={
          typeof window !== "undefined"
            ? localStorage.getItem("selectedSessionId") || ""
            : ""
        }
        userInput={inputContent}
        handleInputChange={handleInputChange}
        handleSubmit={handleSubmit}
        isLoading={isLoading}
        messages={messages}
        appendAndTrigger={async () => {}}
      />
    </div>
  );
}
