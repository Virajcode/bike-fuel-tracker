"use client";

import { cn } from "@/lib/utils";
import { ArrowUp, Square } from "lucide-react";
import { useRef } from "react";
import Textarea from "react-textarea-autosize";
import { Button } from "@/components/ui/button";
import { Message } from "@/lib/types";
import { SuggestedActions } from "@/components/suggested-actions";

interface ChatInputProps {
  chatId: string;
  userInput: string;
  handleInputChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  isLoading: boolean;
  messages: Message[] | undefined;
  appendAndTrigger: (message: Message) => Promise<void>;
}

export function ChatInput({
  chatId,
  userInput,
  handleInputChange,
  handleSubmit,
  isLoading,
  messages,
  appendAndTrigger,
}: ChatInputProps) {
  const inputRef = useRef<HTMLTextAreaElement>(null);

  return (
    <div
      className={cn(
        "mx-auto w-full",
        messages !== undefined && messages.length > 0
          ? "fixed bottom-0 left-0 right-0 bg-background"
          : "fixed bottom-8 left-0 right-0 top-6 flex flex-col items-center justify-center"
      )}
    >
      <form
        onSubmit={handleSubmit}
        className={cn(
          "max-w-3xl w-full mx-auto",
          messages !== undefined && messages.length > 0 ? "px-2 py-4" : "px-6"
        )}
      >
        {messages === undefined ||
          (messages.length === 0 && (
            <div className="mb-6">
              <SuggestedActions/>
            </div>
          ))}
        <div className="relative flex items-center gap-2 bg-muted rounded-3xl border border-input px-4 py-3">
          <Textarea
            ref={inputRef}
            name="input"
            rows={1}
            maxRows={5}
            tabIndex={0}
            placeholder="Enter your discription..."
            spellCheck={false}
            value={userInput}
            className="resize-none w-full bg-transparent border-0 text-sm placeholder:text-muted-foreground focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50"
            onChange={handleInputChange}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                if (userInput.trim().length > 0) {
                  const textarea = e.target as HTMLTextAreaElement;
                  textarea.form?.requestSubmit();
                }
              }
            }}
          />
          <Button
            type={isLoading ? "button" : "submit"}
            size={"icon"}
            variant={"outline"}
            className={cn(isLoading && "animate-pulse", "rounded-full")}
            disabled={userInput.length === 0 && !isLoading}
            onClick={isLoading ? stop : undefined}
          >
            {isLoading ? <Square size={20} /> : <ArrowUp size={20} />}
          </Button>
        </div>
      </form>
    </div>
  );
}
