"use client";

import { ChatInput } from "@/components/chat-input";
import { Message } from "@/lib/types";
import { fillMessageParts, generateUUID } from "@/lib/utils";
import { useCallback, useEffect, useRef, useState, useMemo } from "react";
import useSWR from "swr";
import ChatMessage from "./chat-message";
import { apiClient } from "@/lib/api-client";
import { toast } from "sonner";

export function Chat({ id }: { id: string }) {
  const [inputContent, setInputContent] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // Fetch chat session and history
  const { data: session } = useSWR(`/chat/sessions/${id}`, () => 
    apiClient.chat.getSession(parseInt(id))
  );

  const { data: chatHistory, mutate: mutateHistory } = useSWR(
    `/chat/history/${id}`,
    () => apiClient.chat.getHistory(parseInt(id))
  );

  // Convert chat history to messages format
  const messages = useMemo(() => 
    chatHistory?.flatMap(msg => [
      {
        id: msg.id.toString(),
        content: msg.message,
        role: 'user' as const,
        createdAt: new Date(msg.timestamp),
        parts: [{ type: 'text' as const, text: msg.message }]
      },
      {
        id: `${msg.id}-response`,
        content: msg.response,
        role: 'assistant' as const,
        createdAt: new Date(msg.timestamp),
        parts: [{ type: 'text' as const, text: msg.response }]
      }
    ]) || [],
    [chatHistory]
  );

  // Handle sending messages
  const handleSubmit = useCallback(async (event?: { preventDefault?: () => void }) => {
    event?.preventDefault?.();

    if (!inputContent.trim()) return;

    try {
      setIsLoading(true);
      
      // Create a new message object
      const newMessage: Message = {
        id: generateUUID(),
        content: inputContent,
        role: "user",
        createdAt: new Date(),
        parts: [{ type: 'text' as const, text: inputContent }]
      };

      // Clear input right away for better UX
      setInputContent("");

      // Send message to backend
      const aiResponse = "AI response here"; // Replace with actual AI call
      await apiClient.chat.saveMessage(
        parseInt(id),
        inputContent,
        aiResponse
      );

      // Refresh chat history to show new message
      mutateHistory();
      
    } catch (error) {
      console.error('Failed to send message:', error);
      toast.error("Failed to send message");
    } finally {
      setIsLoading(false);
    }
  }, [id, inputContent, mutateHistory]);

  const handleInputChange = useCallback((e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setInputContent(e.target.value);
  }, []);

  // handle form submission functionality
  const onSubmit = useCallback((e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    handleSubmit();
  }, [handleSubmit]);

  return (
    <div className="flex flex-col w-full max-w-3xl pt-14 pb-10 mx-auto stretch">
      <ChatMessage isLoading={isLoading} messages={messages} />

      <ChatInput
        chatId={id}
        userInput={inputContent}
        handleInputChange={handleInputChange}
        handleSubmit={onSubmit}
        isLoading={isLoading}
        messages={messages} appendAndTrigger={function (message: Message): Promise<void> {
          throw new Error("Function not implemented.");
        } }      />
    </div>
  );
}
