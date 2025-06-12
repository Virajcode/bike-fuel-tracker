"use client";

import { motion } from "framer-motion";
import { Button } from "./ui/button";
import { memo } from "react";
import { Message } from "@/lib/types";
import { generateUUID } from "@/lib/utils";
import { Overview } from "./overview";

interface SuggestedActionsProps {
  chatId: string;
  appendAndTrigger: (message: Message) => Promise<void>;
}

function PureSuggestedActions() {
  const suggestedActions = [
    {
      title: "A quiet cliffside spot overlooking",
      label: "the sea, perfect for watching the sunset.",
      action: "A quiet cliffside spot overlooking the sea, perfect for watching the sunset. There's a bench or space to lay a blanket, with cool breeze, ocean sounds, and no crowds. Bring coffee or snacks, sit close, and enjoy the view as the sky turns gold and pink. Peaceful, romantic, and just the right vibe to unwind together.",
    },
    {
      title: "A cozy outdoor restaurant with warm lighting,",
      label: `big tables, and a relaxed vibe — perfect for family dinner.`,
      action: `A cozy outdoor restaurant with warm lighting, big tables, and a relaxed vibe — perfect for family dinner. The menu has something for everyone, from comfort food to kids' favorites. Laughter, good conversation, and shared plates make it feel just like home, but with no dishes to wash.`,
    },
    // {
    //   title: "Help me write an essay",
    //   label: `about silicon valley`,
    //   action: `Help me write an essay about silicon valley`,
    // },
    // {
    //   title: "What is the weather",
    //   label: "in San Francisco?",
    //   action: "What is the weather in San Francisco?",
    // },
  ];

  return (
    <div className="flex flex-col items-center gap-2 w-full max-w-3xl mx-auto p-4">
      {/* Overview Section */}
      <Overview />
      <div className="grid sm:grid-cols-1 gap-2 w-full">
        {suggestedActions.map((suggestedAction, index) => (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            transition={{ delay: 0.05 * index }}
            key={`suggested-action-${suggestedAction.title}-${index}`}
            className={index > 1 ? "hidden sm:block" : "block"}
          >
            <Button
              variant="ghost"
              className="text-left border rounded-xl px-4 py-3.5 text-sm flex-1 gap-1 sm:flex-col w-full h-auto justify-start items-start"
            >
              <span className="font-medium">{suggestedAction.title}</span>
              <span className="text-muted-foreground">
                {suggestedAction.label}
              </span>
            </Button>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

export const SuggestedActions = memo(PureSuggestedActions, () => true);
